from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def generate_pdf_report(
    filename,
    candidate_name,
    job_role,
    total_score,
    max_score,
    percentage,
    recommendation,
    feedback_report
):
    doc = SimpleDocTemplate(filename)

    elements = []

    elements.append(
        Paragraph("<b>AI Interview Report</b>", styles["Title"])
    )

    elements.append(
        Paragraph(f"<b>Candidate:</b> {candidate_name}", styles["Normal"])
    )

    elements.append(
        Paragraph(f"<b>Job Role:</b> {job_role}", styles["Normal"])
    )

    elements.append(
        Paragraph(
            f"<b>Score:</b> {total_score} / {max_score}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Percentage:</b> {percentage}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Recommendation:</b> {recommendation}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph("<br/><b>AI Feedback</b>", styles["Heading2"])
    )

    for item in feedback_report:

        elements.append(
            Paragraph(
                f"<b>Question:</b> {item['question']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Answer:</b> {item['answer']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Score:</b> {item['score']}/5",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Feedback:</b> {item['feedback']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph("<br/>", styles["Normal"])
        )

    doc.build(elements)

    return filename