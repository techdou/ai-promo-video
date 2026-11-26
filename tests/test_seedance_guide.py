"""Execute the polling example as documented, without any network access."""

import re
import unittest
from pathlib import Path
from unittest.mock import Mock, call

GUIDE = Path(__file__).resolve().parents[1] / "references" / "seedance-guide.md"


class SeedanceGuideTests(unittest.TestCase):
    def setUp(self):
        text = GUIDE.read_text(encoding="utf-8")
        polling = text.split("### Task polling\n", 1)[1].split("## Pricing", 1)[0]
        self.assertEqual(
            set(re.findall(r"^\| `([a-z]+)` \|", polling, re.MULTILINE)),
            {"succeeded", "failed", "cancelled", "expired"},
        )
        example, = re.findall(r"^```python\n(.*?)^```$", polling, re.MULTILINE | re.DOTALL)
        namespace = {}
        exec(compile(example, str(GUIDE), "exec"), namespace)
        self.sleep = namespace["sleep"] = Mock()
        self.wait = namespace["wait_for_video"]

    def test_succeeded_returns_the_video_url_after_pending_states(self):
        url = "https://cdn.example.test/result.mp4"
        get = Mock(side_effect=[
            {"status": "queued"}, {"status": "running"},
            {"status": "succeeded", "content": {"video_url": url}},
        ])
        self.assertEqual(self.wait(get, "task-test"), url)
        self.assertEqual(get.call_args_list, [call("task-test")] * 3)
        self.assertEqual(self.sleep.call_args_list, [call(12)] * 2)

    def test_unsuccessful_terminal_states_stop_immediately(self):
        for status in ("failed", "cancelled", "expired"):
            with self.subTest(status=status):
                get = Mock(return_value={"status": status})
                with self.assertRaisesRegex(RuntimeError, f"task-test.*{status}"):
                    self.wait(get, "task-test")
                get.assert_called_once_with("task-test")
                self.sleep.assert_not_called()

    def test_succeeded_without_url_is_a_delivery_error(self):
        with self.assertRaisesRegex(RuntimeError, "without content.video_url"):
            self.wait(Mock(return_value={"status": "succeeded"}), "task-test")

    def test_nonterminal_polls_are_bounded(self):
        get = Mock(return_value={"status": "running"})
        with self.assertRaisesRegex(TimeoutError, "task-test"):
            self.wait(get, "task-test", max_attempts=2)
        self.assertEqual(get.call_count, 2)
        self.sleep.assert_called_once_with(12)

    def test_completed_is_not_an_ark_status(self):
        with self.assertRaisesRegex(RuntimeError, "unexpected status 'completed'"):
            self.wait(Mock(return_value={"status": "completed"}), "task-test")
        self.sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main()
