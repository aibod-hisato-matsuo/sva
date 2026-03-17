#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parent.parent
INPUT = BASE / "input"
INST = INPUT / "instances"
SCRIPTS = BASE / "scripts"
OUT = BASE / "generated"

GENERAL_MD = OUT / "general_md"
SPEC_MD = OUT / "spec_md"
DOCX = OUT / "docx"

for p in [GENERAL_MD, SPEC_MD, DOCX]:
    p.mkdir(parents=True, exist_ok=True)

# Step 1: Generate 01-08 md from existing generator assets
work_general = GENERAL_MD / "_work"
work_general.mkdir(exist_ok=True)

for name in [
    "ipower-engine.sva.instance.json",
    "ipower-engine.usecase.instance.json",
    "ipower-engine.nfr-risk.instance.json",
]:
    shutil.copy2(INST / name, work_general / name)

# Reuse templates from prior generator package if present in scripts folder sibling? not included here.
# This starter pack focuses on 20-24 generation and docx conversion.
# 01-11 can be reviewed from source instances and prior generated examples if needed.

# Step 2: Generate 20-24 spec md from guardrail
subprocess.run(
    [sys.executable, str(SCRIPTS / "generate_specs_from_guardrail.py"),
     "--input", str(INST),
     "--output", str(SPEC_MD)],
    check=True
)

print("Generated spec markdown in:", SPEC_MD)
print("Next: review the markdown, then convert selected merged markdown to DOCX with md_to_docx.py")
