"""
Task definitions for the Email Triage Environment.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class Email:
    email_id: str
    subject: str
    sender: str
    body: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    ground_truth_classification: str = ""
    ground_truth_action: str = ""

@dataclass
class TaskDefinition:
    id: str
    name: str
    description: str
    difficulty: str
    emails: List[Email]

def grade_triage(action: Dict[str, Any], ground_truth: Email) -> float:
    """
    Grader for a single email triage action.
    Returns:
        0.99 for perfect match
        0.60 for partial match (classification correct, action wrong)
        0.30 for mixed match (classification wrong, action correct - if even possible logic-wise)
        0.05 for complete mismatch
    """
    cls_match = action.get("classification") == ground_truth.ground_truth_classification
    act_match = action.get("action") == ground_truth.ground_truth_action
    
    if cls_match and act_match:
        return 0.99
    if cls_match:
        return 0.60
    if act_match:
        return 0.30
    return 0.05

TASKS: Dict[str, TaskDefinition] = {
    "task1": TaskDefinition(
        id="task1",
        name="Obvious Spam Detection",
        description="Classify obvious spam emails and delete them.",
        difficulty="easy",
        emails=[
            Email(
                email_id="t1_e1",
                subject="Win $1,000,000 NOW!!!",
                sender="noreply@scam-winnerz.com",
                body="Congratulations! You have been selected as the winner of our grand lottery. Click here to claim your $1M cash prize!",
                ground_truth_classification="SPAM",
                ground_truth_action="DELETE"
            ),
            Email(
                email_id="t1_e2",
                subject="Enlarge your productivity with our new tool",
                sender="marketing@sketchy-software.biz",
                body="Boost your team's workflow by 1000% with our patented secret algorithm. Buy now for only $49.99!",
                ground_truth_classification="SPAM",
                ground_truth_action="DELETE"
            ),
            Email(
                email_id="t1_e3",
                subject="Re: Project Update",
                sender="colleague@company.com",
                body="Hi, I've updated the project timeline. Let me know if you have any questions.",
                ground_truth_classification="HAM",
                ground_truth_action="KEEP"
            ),
            Email(
                email_id="t1_e4",
                subject="Your account will be suspended",
                sender="support@not-really-your-bank.net",
                body="Security alert: Unusual activity detected. Please login at http://fake-bank-login.com to verify your identity.",
                ground_truth_classification="SPAM",
                ground_truth_action="DELETE"
            ),
            Email(
                email_id="t1_e5",
                subject="Cheap meds delivered to your door",
                sender="sales@online-pharmacy-global.xyz",
                body="Get high quality medications at a fraction of the cost. No prescription needed!",
                ground_truth_classification="SPAM",
                ground_truth_action="DELETE"
            )
        ]
    ),
    "task2": TaskDefinition(
        id="task2",
        name="Phishing Detection",
        description="Identify phishing attempts and report them.",
        difficulty="medium",
        emails=[
            Email(
                email_id="t2_e1",
                subject="Microsoft Security Alert: Microsoft account unusual sign-in activity",
                sender="account-security-noreply@microsoft.com.security-update.info",
                body="We detected something unusual about a recent sign-in for the Microsoft account. Please click here to review.",
                ground_truth_classification="PHISHING",
                ground_truth_action="REPORT"
            ),
            Email(
                email_id="t2_e2",
                subject="Urgent: Unauthorised Transaction Detected",
                sender="alert@paypal-secure-check.com",
                body="Someone tried to spend $500 from your account. If this wasn't you, log in immediately to cancel the transaction.",
                ground_truth_classification="PHISHING",
                ground_truth_action="REPORT"
            ),
            Email(
                email_id="t2_e3",
                subject="Invitation to Interview",
                sender="hr@legit-recruitment.com",
                body="We loved your profile! Can you join us for an interview next Wednesday at 10 AM?",
                ground_truth_classification="HAM",
                ground_truth_action="KEEP"
            ),
            Email(
                email_id="t2_e4",
                subject="Shared document: '2024 Payroll List'",
                sender="ceo.office@google-drive-share.co",
                body="The CEO has shared a sensitive document with you. Please sign in to view it.",
                ground_truth_classification="PHISHING",
                ground_truth_action="REPORT"
            ),
            Email(
                email_id="t2_e5",
                subject="Action required: Update your payment method",
                sender="billing@netflix-account-update.tv",
                body="Your subscription is about to expire because your current payment method failed. Update it now to keep watching.",
                ground_truth_classification="PHISHING",
                ground_truth_action="REPORT"
            )
        ]
    ),
    "task3": TaskDefinition(
        id="task3",
        name="Spear Phishing Detection",
        description="Detect sophisticated targeted spear phishing.",
        difficulty="hard",
        emails=[
            Email(
                email_id="t3_e1",
                subject="Confidential: Draft Merger Agreement",
                sender="james.wilson.legal@company-partner.com",
                body="Hi team, James here. Attached is the sensitive draft for the Acme Corp merger. Please escalate to the board immediately if you see any dealbreakers.",
                ground_truth_classification="PHISHING",
                ground_truth_action="ESCALATE"
            ),
            Email(
                email_id="t3_e2",
                subject="Internal Memo: Leadership Changes",
                sender="corporate-comms@company-intranet.net",
                body="The board has announced new leadership changes. Follow the link to read the internal memo.",
                ground_truth_classification="PHISHING",
                ground_truth_action="ESCALATE"
            ),
            Email(
                email_id="t3_e3",
                subject="Lunch tomorrow?",
                sender="sarah.jones@colleague-personal.com",
                body="Hey! Want to grab lunch at that new place around the corner tomorrow?",
                ground_truth_classification="HAM",
                ground_truth_action="KEEP"
            ),
            Email(
                email_id="t3_e4",
                subject="Urgent Action: Wire Transfer Verification #88219",
                sender="finance.controller@company-global-ops.com",
                body="I need you to verify this wire transfer for the Hong Kong office urgently. The beneficiary details are attached in the doc.",
                ground_truth_classification="PHISHING",
                ground_truth_action="ESCALATE"
            ),
            Email(
                email_id="t3_e5",
                subject="System Maintenance Notification",
                sender="it-support@company-tech-portal.org",
                body="The main server will be down for maintenance this Sunday. Please ensure all your work is synced.",
                ground_truth_classification="PHISHING",
                ground_truth_action="ESCALATE"
            )
        ]
    )
}
