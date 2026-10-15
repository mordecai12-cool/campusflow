"""Original persistence tests plus AI-assisted safety regression coverage."""
from copy import deepcopy
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import tempfile
import unittest
from unittest.mock import patch

from campusflow.storage import StorageError, load_tickets, save_tickets
from campusflow.tickets import _find_record, create_ticket, add_note
from campusflow.workflow import assign_ticket, update_status


class TestStorage(unittest.TestCase):

    def test_save_and_load(self):
        tickets = [
            {
                "id": "T001",
                "title": "Network issue",
                "notes": [],
                "category": "Network",
                "urgency": "high",
                "affected_users": 10,
                "priority": "critical",
                "status": "open",
                "assigned_to": None
            }
        ]

        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "tickets.json")
            save_tickets(tickets, filename)
            loaded = load_tickets(filename)
            self.assertEqual(loaded, tickets)

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "missing.json")
            self.assertEqual(load_tickets(filename), [])

    def test_invalid_json_raises_error(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
            file.write("this is not valid json")
            filename = file.name

        with self.assertRaises(ValueError):
            load_tickets(filename)

        os.remove(filename)



class StorageTests(unittest.TestCase):

    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'data' / 'tickets.json'
        self.tickets = []
        create_ticket('Café Wi-Fi', 'Network', 'high', 12, self.tickets)

    def write_raw(self, content):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(content, encoding='utf-8')

    def test_missing_file_starts_fresh_without_creating_file(self):
        self.assertEqual(load_tickets(self.path), [])
        self.assertFalse(self.path.exists())

    def test_json_round_trip_preserves_all_fields(self):
        assign_ticket(self.tickets, 'T001', 'Demo Staff')
        update_status(_find_record(self.tickets, 'T001'), 'in_progress')
        update_status(_find_record(self.tickets, 'T001'), 'resolved')
        save_tickets(self.tickets, self.path)
        self.assertEqual(load_tickets(self.path), self.tickets)
        self.assertIn('Café', self.path.read_text(encoding='utf-8'))

    def test_creation_after_reload_does_not_duplicate_ids(self):
        self.tickets[0]['id'] = 'T999'
        save_tickets(self.tickets, self.path)
        loaded = load_tickets(self.path)
        ticket = create_ticket('Restart issue', 'Other', 'low', 1, loaded)
        self.assertEqual(ticket['id'], 'T1000')
        self.assertEqual(len({t['id'] for t in loaded}), 2)
        save_tickets(loaded, self.path)
        self.assertEqual(load_tickets(self.path), loaded)

    def test_corrupted_json_is_not_changed(self):
        self.write_raw('{"broken":')
        before = self.path.read_bytes()
        with self.assertRaisesRegex(StorageError, 'Cannot load'):
            load_tickets(self.path)
        with self.assertRaisesRegex(StorageError, 'Cannot save'):
            save_tickets(self.tickets, self.path)
        self.assertEqual(self.path.read_bytes(), before)

    def test_invalid_record_shapes_and_types_rejected(self):
        values = ({}, None, 7, [None], [{}])
        for value in values:
            with self.subTest(value=value):
                self.write_raw(json.dumps(value))
                before = self.path.read_bytes()
                with self.assertRaises(StorageError):
                    load_tickets(self.path)
                self.assertEqual(self.path.read_bytes(), before)

    def test_inconsistent_records_rejected_without_overwriting(self):
        invalid = ({'affected_users': True}, {'affected_users': 0}, {'affected_users': 1.2}, {'category': 'invalid'}, {'urgency': 'HIGH'}, {'priority': 'low'}, {'status': 'closed'}, {'status': 'in_progress'}, {'status': 'resolved'}, {'assigned_to': ' '}, {'assigned_to': 7}, {'id': 'T000'}, {'title': ' '}, {'extra': 'unexpected'})
        for change in invalid:
            with self.subTest(change=change):
                broken = deepcopy(self.tickets)
                broken[0].update(change)
                self.write_raw(json.dumps(broken))
                before = self.path.read_bytes()
                with self.assertRaises(StorageError):
                    load_tickets(self.path)
                with self.assertRaises(StorageError):
                    save_tickets(self.tickets, self.path)
                self.assertEqual(self.path.read_bytes(), before)

    def test_duplicate_ids_and_json_keys_are_rejected(self):
        duplicate = self.tickets + deepcopy(self.tickets)
        self.write_raw(json.dumps(duplicate))
        with self.assertRaisesRegex(StorageError, 'unique'):
            load_tickets(self.path)
        raw = json.dumps(self.tickets).replace('"id": "T001"', '"id": "T001", "id": "T002"')
        self.write_raw(raw)
        with self.assertRaisesRegex(StorageError, 'Duplicate JSON key'):
            load_tickets(self.path)

    def test_invalid_utf8_is_reported(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_bytes(b'\xff\xfe')
        before = self.path.read_bytes()
        with self.assertRaises(StorageError):
            load_tickets(self.path)
        self.assertEqual(self.path.read_bytes(), before)

    def test_invalid_save_does_not_touch_existing_data(self):
        save_tickets(self.tickets, self.path)
        before = self.path.read_bytes()
        invalid = deepcopy(self.tickets)
        invalid[0]['affected_users'] = False
        with self.assertRaises(StorageError):
            save_tickets(invalid, self.path)
        self.assertEqual(self.path.read_bytes(), before)

    def test_failed_atomic_replace_preserves_original_and_cleans_temporary_file(self):
        save_tickets(self.tickets, self.path)
        before = self.path.read_bytes()
        create_ticket('Another', 'Other', 'low', 1, self.tickets)
        with patch('campusflow.storage.os.replace', side_effect=OSError('simulated write failure')):
            with self.assertRaisesRegex(StorageError, 'simulated write failure'):
                save_tickets(self.tickets, self.path)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.path.parent.glob('*.tmp')), [])
        self.assertEqual(list(self.path.parent.glob('.*.tmp')), [])

    def test_empty_collection_round_trip(self):
        save_tickets([], self.path)
        self.assertEqual(load_tickets(self.path), [])

    def test_non_file_storage_path_is_reported(self):
        self.path.mkdir(parents=True)
        with self.assertRaises(StorageError):
            load_tickets(self.path)
        with self.assertRaises(StorageError):
            save_tickets(self.tickets, self.path)

    def test_save_load_preserves_notes_and_next_note_id(self):
        add_note(self.tickets, 'T001', 'Ina', 'First note')

        save_tickets(self.tickets, self.path)

        loaded = load_tickets(self.path)

        self.assertEqual(loaded[0]['notes'][0]['note_id'], 'N001')
        self.assertEqual(loaded[0]['notes'][0]['author'], 'Ina')
        self.assertEqual(loaded[0]['notes'][0]['message'], 'First note')

        add_note(loaded, 'T001', 'Marvellous', 'Second note')

        self.assertEqual(loaded[0]['notes'][1]['note_id'], 'N002')

    def test_invalid_notes_are_rejected_without_overwriting(self):
        broken = deepcopy(self.tickets)
        broken[0]["notes"] = [
            {
                "note_id": "N001",
                "author": "Ina",
                "message": "Good note"
            },
            {
                "note_id": "N001",
                "author": "Marvellous",
                "message": "Duplicate ID"
            }
        ]

        self.write_raw(json.dumps(broken))
        before = self.path.read_bytes()

        with self.assertRaises(StorageError):
            load_tickets(self.path)

        self.assertEqual(self.path.read_bytes(), before)