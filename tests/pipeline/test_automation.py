from unittest.mock import MagicMock

from app.pipeline.automation import AutomationPipeline


def test_pipeline_runs():
    gmail = MagicMock()
    summarizer = MagicMock()
    generator = MagicMock()
    formatter = MagicMock()

    email = MagicMock()
    analysis = MagicMock()
    digest = MagicMock()

    gmail.iter_unread_emails.return_value = [
        email,
    ]

    summarizer.summarize.return_value = analysis

    generator.generate.return_value = digest

    formatter.format.return_value = "Digest"

    pipeline = AutomationPipeline(
        gmail=gmail,
        summarizer=summarizer,
        generator=generator,
        formatter=formatter,
    )

    pipeline.run()

    gmail.iter_unread_emails.assert_called_once()

    summarizer.summarize.assert_called_once_with(
        email,
    )

    gmail.mark_as_read.assert_called_once_with(
        email.id,
    )

    generator.generate.assert_called_once_with(
        [analysis],
    )

    formatter.format.assert_called_once_with(
        digest,
    )
