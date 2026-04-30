# Title
fix: Add TencentSearch compatibility guard for lagent version (InternLM#288)

## Related Issue
- https://github.com/InternLM/MindSearch/issues/288

## Background
Running:

`python -m mindsearch.app --lang cn --model_format internlm_silicon --search_engine TencentSearch`

could fail with:

`NameError: name 'TencentSearch' is not defined`

from `lagent/actions/bing_browser.py` when `lagent` is below the version that introduced `TencentSearch`.

## Root Cause
- `TencentSearch` is not available in older `lagent` versions.
- The browser action resolves the searcher class name dynamically, so older environments raise `NameError` at runtime.
- The resulting error message does not clearly tell users the fix path.

## What Changed
### 1) Add a TencentSearch-specific lagent version check
In `mindsearch/agent/__init__.py`:
- introduce `MIN_TENCENTSEARCH_LAGENT_VERSION = "0.5.0rc2"`
- add `_validate_tencentsearch_lagent_version(...)` helper to centralize guard logic
- call this helper before plugin creation in `init_agent(...)`
- raise a clear `RuntimeError` with an upgrade command when incompatible
- gracefully ignore unparsable version strings (`InvalidVersion`) to preserve existing fallback behavior

### 2) Add version parsing dependency
In `requirements.txt`:
- add `packaging` for robust semantic version comparison

### 3) Add targeted unit tests
In `tests/test_tencentsearch_version_check.py`:
- verify old lagent versions raise `RuntimeError` for TencentSearch
- verify required/minimum version passes
- verify non-Tencent engines skip version enforcement
- verify invalid version strings do not crash validation

## User-facing Impact
- TencentSearch users on incompatible lagent now get an actionable initialization error instead of a confusing `NameError`.
- Non-Tencent search engines remain unaffected.

## Validation
### Repro (before fix)
1. Install an older lagent (e.g. `<0.5.0rc2`)
2. Run TencentSearch startup command
3. Observe `NameError` from `eval(searcher_type)` path

### Verify (after fix)
1. With old lagent + TencentSearch:
   - Expect clear `RuntimeError`:
   - `TencentSearch requires lagent >= 0.5.0rc2 ... Please upgrade: pip install lagent==0.5.0rc2`
2. With `lagent==0.5.0rc2` + TencentSearch:
   - Expect normal initialization
3. With old lagent + non-Tencent engine:
   - Expect existing behavior (no Tencent-specific guard triggered)
4. Run unit tests:
   - `python -m unittest tests.test_tencentsearch_version_check`

## Risk Assessment
- Low risk: change is scoped to TencentSearch initialization path.
- No behavioral changes for existing non-Tencent flows.

## Getting TencentSearch API Credentials

To use TencentSearch, you need to obtain API credentials from Tencent Cloud:

### Step 1: Create Tencent Cloud Account
1. Visit https://cloud.tencent.com/
2. Sign up for a Tencent Cloud account
3. Complete account verification

### Step 2: Enable Tencent Search Service
1. Go to the Tencent Cloud Console
2. Navigate to "Tencent Search" (腾讯搜索) service
3. Enable the service (may require application approval)

### Step 3: Get API Credentials
1. In the Tencent Cloud Console, go to "Access Management" (访问管理)
2. Navigate to "API Keys" (API密钥)
3. Create a new secret key or use existing one
4. Copy the following values:
   - **SecretId**: Your API access key ID
   - **SecretKey**: Your API secret key

### Step 4: Configure Environment Variables

```bash
# Set environment variables (add to ~/.bashrc or ~/.zshrc for persistence)
export TENCENT_SEARCH_SECRET_ID="your_secret_id_here"
export TENCENT_SEARCH_SECRET_KEY="your_secret_key_here"
```

### Step 5: Verify Configuration

```bash
# Check if variables are set
echo $TENCENT_SEARCH_SECRET_ID
echo $TENCENT_SEARCH_SECRET_KEY

# Test with MindSearch
pip install lagent==0.5.0rc2
python -m mindsearch.app --lang cn --model_format internlm_silicon --search_engine TencentSearch
```

### Troubleshooting

If you get authentication errors:
1. Verify your credentials are correct
2. Check if Tencent Search service is enabled
3. Ensure your account has sufficient permissions
4. Check if there are any billing/quota limits

## Files in this PR
- `mindsearch/agent/__init__.py` - Version check implementation
- `requirements.txt` - Added packaging dependency
- `PR_288_DESCRIPTION.md` - This file
- `tests/test_tencentsearch_version_check.py` - Unit tests
- `TESTING_GUIDE.md` - Comprehensive testing instructions
- `test_version_check.py` - Validation script
