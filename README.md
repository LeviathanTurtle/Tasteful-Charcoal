# Tasteful Charcoal
A tool that displays a mod's supported modloaders and versions given a list of mod IDs. This <b>does not</b> auto-fetch a mod's dependencies. This has only been tested with Minecraft, but theoretically should work with any game registered on CurseForge.

## Requirements
- Python 3.10+
- A [CurseForge API key](https://support.curseforge.com/en/support/solutions/articles/9000208346-about-the-curseforge-api-and-how-to-apply-for-a-key#key)

## Usage
1. Create a `.env` file and add the following line: `CURSEFORGE_API_KEY="your_api_key"`.
2. Fill out `config.py`.
3. Run `python tasteful_charcoal.py`.

