from __future__ import annotations

from benchling_sdk.apps.status.types import ReferencedSessionLinkType


def ref(reference: ReferencedSessionLinkType) -> str:
    """
    Ref.

    Helper method for easily serializing a referenced object into a string embeddable in AppSessionMessageCreate
    content.

    Example:
        dna_sequence = benchling.dna_sequences.get_by_id("seq_1234")
        AppSessionMessageCreate(f"This is my DNA sequence {ref(dna_sequence)} for analysis"
    """
    # Not sure {} are possible in Benchling IDs, but the spec says we're escaping
    unescape_id = reference.id
    escaped_id = unescape_id.replace("{", "\\{").replace("}", "\\}")
    return f"{{id:{escaped_id}}}"
