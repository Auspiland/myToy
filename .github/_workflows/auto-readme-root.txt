name: Auto Update Root README

on:
  schedule:
    - cron: "2 3 * * *"      # 매일 12:02 KST = 03:02 UTC (프로젝트 README 업데이트 2분 후)
    - cron: "2 10 * * *"     # 매일 19:02 KST = 10:02 UTC
  workflow_dispatch:          # 수동 실행도 가능

permissions:
  contents: write

concurrency:
  group: readme-updates
  cancel-in-progress: false

env:
  README_PATH: "README.md"
  SECTION_START: "<!-- AUTO-UPDATE:START -->"
  SECTION_END: "<!-- AUTO-UPDATE:END -->"
  LAST_SHA_START: "<!-- LAST_PROCESSED_SHA:"
  LLM_MODEL: gpt-5-mini
  PROJECT_DIRS: "geo_map,Mini-Pipeline,B_project"

jobs:
  update-readme:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install openai==1.* gitpython==3.* tenacity==8.*

      - name: Run updater
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python .github/scripts/update_readme_root.py \
            --readme "$README_PATH" \
            --llm-model "$LLM_MODEL" \
            --section-start "$SECTION_START" \
            --section-end "$SECTION_END" \
            --last-sha-start "$LAST_SHA_START" \
            --project-dirs "$PROJECT_DIRS"

      - name: Commit & Push if changed
        run: |
          if [[ -n "$(git status --porcelain)" ]]; then
            git config user.name "readme-bot"
            git config user.email "readme-bot@users.noreply.github.com"
            git add -A
            git commit -m "chore(root): auto-update README via LLM [skip ci]"
            git push
          else
            echo "No changes to commit."
          fi
