from typing import List

from pydantic.main import BaseModel


class Vuln(BaseModel):
    cwe: str
    bug_msg: str
    start: int
    end: int


class VulnFile(BaseModel):
    path: str
    src: str
    vulns: List[Vuln]
    is_obfuscated: bool = False

class PatchMessage(BaseModel):
    title: str
    msg: str
    start_line: int
    end_line: int


class Patch(BaseModel):
    path: str
    patch: str
    msgs: List[PatchMessage] = []


class CreatePullRequest(BaseModel):
    repo_slug: str
    path: str
    diff_text: str
    original_branch_name: str
    next_branch_name: str
    applied_patches: List[Patch]
