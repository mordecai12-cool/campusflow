# Pull requests and team workflow

Repository: https://github.com/mordecai12-cool/campusflow2

| PR | Author | Verified state | Evidence limitation |
| --- | --- | --- | --- |
| [#1 Complete CampusFlow helpdesk system](https://github.com/mordecai12-cool/campusflow2/pull/1) | mordecai12-cool | Merged into main by miikese; no recorded reviews | The diff deletes five cache files. Application and tests were already on main; this is not a reviewed feature contribution. |
| [#2 Fix ticket lifecycle, validation and persistence; add clone launcher and tests](https://github.com/mordecai12-cool/campusflow2/pull/2) | miikese | Merged at Michael's explicit request after passing checks; no recorded partner approval | AI-assisted application and tests; publication does not establish genuine peer review. |
| [#8 Combine actual campus source with shared CampusFlow app](https://github.com/mordecai12-cool/campusflow2/pull/8) | miikese | Actual source-folder integration and 95-test evidence published | AI-assisted transfer/adaptation at Michael's explicit merge request; no independent human review is claimed. |
| [#9 Isolate ticket IDs and lifecycle validation](https://github.com/mordecai12-cool/campusflow2/pull/9) | miikese | Open proposal with 97 passing branch tests; partner review required before merge | Assistant-authored refactors/tests and accurate provenance; personal learning and independent contributions remain outstanding. |

The PR list was verified directly: repository search omitted PR #1 even though
it exists. Historical approval cannot be supplied after a merge and described
as pre-merge approval. A further genuine feature-and-test PR from Mordecai is
needed to establish the guide's reviewed contribution requirement.
See [assistant review findings](review-findings.md) and
[submission state](submission.md). Assistant findings are not human reviews.

Integration branch: `feat/engineer-b-integration-and-checks`, authored under
Michael's account with explicit AI-assistance attribution. Original Mordecai
commits are preserved. [PR #2](https://github.com/mordecai12-cool/campusflow2/pull/2)
is merged into main, authored by miikese. Merge commit:
7fa245cf13e8567557f3dbd9e5cdec8aa9b38b18. Michael explicitly requested
publication after successful checks; no partner approval is claimed.
The PR title and body are also recorded in [pr-draft.md](pr-draft.md).

## Create a pull request yourself

1. Make your code and matching test changes on a feature branch.
2. Run the tests and inspect git diff.
3. Commit and push the branch under your own GitHub account.
4. Open the repository on GitHub and click **Compare & pull request**.
5. Set **base** to `main` and **compare** to your feature branch.
6. Describe the problem, resulting behavior, actual test results and AI assistance.
7. Click **Create pull request** and ask your partner to review it.
8. Fix review findings on the same branch; pushing updates the PR automatically.
9. Merge after genuine approval and successful checks.

For this branch, the comparison page is:
https://github.com/mordecai12-cool/campusflow2/compare/main...feat/engineer-b-integration-and-checks

To contribute a later change from a clean local clone:

```sh
git switch main
git pull --ff-only
git switch -c feat/your-change
# Implement application code and matching tests yourself.
python3 -m unittest discover -s tests -v
git diff --check
git add <the-files-you-changed>
git commit -m "Describe your actual change"
git push -u origin feat/your-change
```

## Real review and contribution evidence

Genuine partner approval and cross-review remain incomplete. Do not paste invented findings
or approvals. Record each person's actual PR, meaningful changes, tests and
learning evidence. An AI-generated commit is not proof of independent work.

## Publish the finished local commits

On the computer containing this checkout, authenticate Git to GitHub using
your own account, then run:

```sh
cd /home/student/campusflow2
git switch feat/engineer-b-integration-and-checks
python3 -m unittest discover -s tests -v
git push -u origin feat/engineer-b-integration-and-checks
```

This branch has already been pushed using Michael's authenticated GitHub CLI.
The shell checkout is separate from the original /home/student/campus project.
If using the portable Git bundle on another computer, clone campusflow2 first,
then fetch the feature branch from the bundle file:

```sh
git clone https://github.com/mordecai12-cool/campusflow2.git
cd campusflow2
git fetch /path/to/campusflow2-commits.bundle feat/engineer-b-integration-and-checks:feat/engineer-b-integration-and-checks
git switch feat/engineer-b-integration-and-checks
python3 -m unittest discover -s tests -v
git push -u origin feat/engineer-b-integration-and-checks
```

Replace /path/to with the actual download location. Once pushed, open the
comparison link above, click Create pull request, and use pr-draft.md.
The connected plugin initially returned 403 when creating a branch. Michael
completed GitHub CLI sign-in under his own account, and the assistant then
published the branch and created PR #2. No login to the owner's account was used.
