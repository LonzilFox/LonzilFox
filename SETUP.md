# Profile README — Setup

This is the `LonzilFox/LonzilFox` profile repository. Keep the root `README.md`, `scripts/sync_repos.py`, and `.github/workflows/sync-profile.yml` together.

## First deployment

1. Push all files (including the hidden `.github` directory) to the **public** `LonzilFox/LonzilFox` repository's default **main** branch.
2. Go to **Actions → Sync profile README → Run workflow → Run workflow**. The first run populates the initially empty Projects section.
3. Check the run's status. In the `Rebuild project list from public GitHub Topics` step, confirm that the expected number of public repositories was collected. In `Commit and push updated README`, confirm that the generated README was pushed.
4. If the push fails, open **Settings → Actions → General → Workflow permissions** and allow **Read and write permissions**, if your repository policy permits it. Also check whether branch protection prevents bot pushes.

## Updates

- New public repositories or changes to Topics are found on the next scheduled GitHub Actions run (nominally **every 15 minutes**, subject to GitHub delays). Creating a repository elsewhere does **not** trigger this workflow immediately.
- For an immediate update, click **Actions → Sync profile README → Run workflow**.
- A regular push to the profile repository's `main` branch also triggers synchronization.
- Private repositories are never listed. Public repositories without `category-*` Topics appear under **Unclassified**.
- GitHub can suspend scheduled runs after 60 days of inactivity in public repositories. This workflow creates a small empty keep-alive commit only if the last commit is at least 35 days old, reducing that risk. If scheduled runs still stop, check the Actions page for a disabled workflow and re-enable it. The first manual run also makes it easy to verify permissions.

Category assignments are controlled only by GitHub repository Topics (`category-tools`, `category-game`, `category-ai`, `category-web`, `category-automation`, `category-creative`, or custom `category-*` Topics). The content between the two `AUTO-PROJECTS` markers is generated; edits outside that region are preserved.

No personal access token or cross-repository write permission is required. The workflow writes only its own `README.md`.
