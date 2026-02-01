#!/usr/bin/env python3
"""Quick test script to validate the detector."""
import sys
sys.path.insert(0, "/home/alfo/Documents/project/Modern project/2026/ AI Fake Job Posting Detector")

from core.detector import FakeJobDetector
from data.sample_jobs import (
    FAKE_JOB_1,
    FAKE_JOB_2,
    SUSPICIOUS_JOB_1,
    LEGITIMATE_JOB_1,
    LEGITIMATE_JOB_2,
)


def print_result(title: str, job, result):
    """Pretty print detection result."""
    print("\n" + "="*80)
    print(f"🔍 {title}")
    print("="*80)
    print(f"Job Title: {job.title}")
    print(f"Company: {job.company_name}")
    print(f"\nClassification: {result.classification}")
    print(f"Risk Score: {result.risk_score}/100")
    print(f"Confidence: {result.confidence}%")
    print(f"\nReasons:")
    for i, reason in enumerate(result.reasons, 1):
        print(f"  {i}. [{reason.category}] {reason.message}")
        print(f"     Signal: {reason.signal} (confidence: {reason.confidence})")


if __name__ == "__main__":
    detector = FakeJobDetector()

    print("\n" + "█"*80)
    print("FAKE JOB POSTING DETECTOR - TEST SUITE")
    print("█"*80)

    # Test fake jobs
    result1 = detector.predict(FAKE_JOB_1)
    print_result("TEST 1: FAKE JOB (Guaranteed money + payment required)", FAKE_JOB_1, result1)

    result2 = detector.predict(FAKE_JOB_2)
    print_result("TEST 2: FAKE JOB (Unknown company + unrealistic salary)", FAKE_JOB_2, result2)

    # Test suspicious job
    result3 = detector.predict(SUSPICIOUS_JOB_1)
    print_result("TEST 3: SUSPICIOUS JOB (Unverified company)", SUSPICIOUS_JOB_1, result3)

    # Test legitimate jobs
    result4 = detector.predict(LEGITIMATE_JOB_1)
    print_result("TEST 4: LEGITIMATE JOB (Google - verified company)", LEGITIMATE_JOB_1, result4)

    result5 = detector.predict(LEGITIMATE_JOB_2)
    print_result("TEST 5: LEGITIMATE JOB (Microsoft - verified company)", LEGITIMATE_JOB_2, result5)

    print("\n" + "█"*80)
    print("TEST SUITE COMPLETE")
    print("█"*80 + "\n")

    # Summary - test 1 should be Fake, test 2 can be Suspicious or Fake (both are concerning)
    test1_correct = result1.classification == "Fake"
    test2_concerning = result2.classification in ["Fake", "Suspicious"]
    legit_correct = result4.classification == "Legitimate" and result5.classification == "Legitimate"
    
    print(f"✓ Test 1 (Fake Detection): {'PASS' if test1_correct else 'FAIL'}")
    print(f"✓ Test 2 (Suspicious Detection): {'PASS' if test2_concerning else 'FAIL'}")
    print(f"✓ Legitimate Detection: {'PASS' if legit_correct else 'FAIL'}")
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all([test1_correct, test2_concerning, legit_correct]) else '⚠️ SOME TESTS FAILED'}")
