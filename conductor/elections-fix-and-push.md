# Elections Fix & Deployment Plan

## Objective
Fix the 404 error occurring on the `elections/summary/` API endpoint by adjusting the URL routing order, ensure `GEMINI.md` is ignored by Git, and deploy the latest changes to both the production server and the remote origin repository.

## Key Files & Context
- `backend/api/urls.py`
- `.gitignore`

## Implementation Steps
1. **Fix URL Routing**: Modify `backend/api/urls.py` to move `path('elections/summary/', views.ElectionSummaryView.as_view(), name='election-summary')` above `path("", include(router.urls))` to prevent the default router from improperly capturing the request.
2. **Update Gitignore**: Append `GEMINI.md` to `.gitignore` to prevent Gemini CLI configuration/history files from being tracked in version control.
3. **Apply Backend Changes**: Run `docker compose restart web` on the server (or locally if applicable) so Django reloads the URL configurations.
4. **Commit & Push**:
   - Stage the changes (`git add .`).
   - Commit the changes (e.g., `git commit -m "Fix elections summary URL routing and ignore GEMINI.md"`).
   - Push to the production server (`git push prod main`).
   - Push to the origin repository (`git push origin main`).

## Verification & Testing
- Ensure the Android app's Elections tab loads successfully without a 404 error.
- Verify `GEMINI.md` is no longer tracked by Git (`git status`).
- Confirm both the `prod` and `origin` remotes received the latest commit.