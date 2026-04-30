import unittest

import mindsearch.agent as agent_init


class TencentSearchVersionCheckTestCase(unittest.TestCase):

    def test_tencentsearch_raises_for_older_lagent_version(self):
        with self.assertRaises(RuntimeError) as context:
            agent_init._validate_tencentsearch_lagent_version(
                "TencentSearch", lagent_version="0.2.0")
        self.assertIn("TencentSearch requires lagent >=", str(context.exception))
        self.assertIn(agent_init.MIN_TENCENTSEARCH_LAGENT_VERSION,
                      str(context.exception))

    def test_tencentsearch_accepts_supported_lagent_version(self):
        agent_init._validate_tencentsearch_lagent_version(
            "TencentSearch",
            lagent_version=agent_init.MIN_TENCENTSEARCH_LAGENT_VERSION)

    def test_non_tencent_engine_skips_validation(self):
        agent_init._validate_tencentsearch_lagent_version(
            "DuckDuckGoSearch", lagent_version="0.0.1")

    def test_invalid_version_string_is_ignored(self):
        agent_init._validate_tencentsearch_lagent_version(
            "TencentSearch", lagent_version="not-a-semver")


if __name__ == "__main__":
    unittest.main()
