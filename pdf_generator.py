from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime
import os


def generate_pdf(chat_history):

    if not os.path.exists("reports"):
        os.makedirs("reports")

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"reports/Health_Report_{timestamp}.pdf"
    )

    document = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "AI Public Health Chatbot Report",
        styles["Title"]
    )

    content.append(title)

    content.append(
        Spacer(1, 20)
    )

    report_date = Paragraph(
        f"Generated On: {datetime.now()}",
        styles["Normal"]
    )

    content.append(report_date)

    content.append(
        Spacer(1, 20)
    )

    if len(chat_history) == 0:

        content.append(
            Paragraph(
                "No chat history available.",
                styles["BodyText"]
            )
        )

    else:

        for index, chat in enumerate(
            chat_history,
            start=1
        ):

            content.append(
                Paragraph(
                    f"<b>Conversation {index}</b>",
                    styles["Heading2"]
                )
            )

            content.append(
                Spacer(1, 10)
            )

            content.append(
                Paragraph(
                    f"<b>Time:</b> {chat['time']}",
                    styles["BodyText"]
                )
            )

            content.append(
                Paragraph(
                    f"<b>Question:</b> {chat['question']}",
                    styles["BodyText"]
                )
            )

            content.append(
                Paragraph(
                    f"<b>Response:</b> {chat['response']}",
                    styles["BodyText"]
                )
            )

            content.append(
                Spacer(1, 15)
            )

        content.append(
            PageBreak()
        )

        content.append(
            Paragraph(
                "Health Awareness Summary",
                styles["Heading1"]
            )
        )

        content.append(
            Spacer(1, 15)
        )

        summary = """
        This report was generated using the
        AI-Driven Public Health Chatbot.

        The information provided is intended
        for educational and awareness purposes
        only and should not be considered
        professional medical advice.

        Users should consult qualified
        healthcare professionals for diagnosis,
        treatment, and medical emergencies.
        """

        content.append(
            Paragraph(
                summary,
                styles["BodyText"]
            )
        )

    document.build(content)

    return filename