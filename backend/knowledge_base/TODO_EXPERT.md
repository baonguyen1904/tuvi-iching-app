# TODO: Expert Review Required

This document lists all Knowledge Base files that currently use **mock/placeholder content** and need expert review before production use.

## Files Needing Expert Review

### Core Files
| File | Status | What's Needed |
|------|--------|---------------|
| `core/scoring_rules.md` | Mock | Verify scoring explanation matches actual system behavior |
| `core/alert_interpretation.md` | Mock | Validate alert level descriptions with expert understanding |
| `core/tone_guidelines.md` | Mock | Expert to refine tone rules, add more forbidden/required phrases |

### Dimension Guides (7 files)
| File | Status | What's Needed |
|------|--------|---------------|
| `dimensions/su_nghiep.md` | Mock | Expert interpretation patterns for Quan Lộc cung |
| `dimensions/tien_bac.md` | Mock | Expert interpretation patterns for Tài Bạch cung |
| `dimensions/hon_nhan.md` | Mock | Expert interpretation patterns for Phu Thê cung |
| `dimensions/suc_khoe.md` | Mock | Expert interpretation patterns for Tật Ách cung |
| `dimensions/dat_dai.md` | Mock | Expert interpretation patterns for Điền Trạch cung |
| `dimensions/hoc_tap.md` | Mock | Expert interpretation patterns for Mệnh cung (học tập) |
| `dimensions/con_cai.md` | Mock | Expert interpretation patterns for Tử Tức cung |

### Star References
| File | Status | What's Needed |
|------|--------|---------------|
| `stars/chinh_tinh.md` | Mock (skeleton) | Detailed descriptions of 14 major stars with specific patterns |
| `stars/phu_tinh.md` | Mock (skeleton) | More complete minor star descriptions |

### Example Outputs
| File | Status | What's Needed |
|------|--------|---------------|
| `examples/approved_outputs/sample_su_nghiep.md` | Mock | Expert to review and approve as reference output |
| (missing) `examples/approved_outputs/sample_tien_bac.md` | Not created | Expert to provide approved example for Tiền Bạc |
| (missing) Other dimensions | Not created | Expert to provide 1-2 more approved examples |

## How to Replace Mock Content

1. Read the current mock file to understand the structure
2. Replace content with real expert knowledge while keeping the same markdown format
3. Run tests to verify KB still loads: `cd backend && python -m pytest tests/test_ai_kb.py -v`
4. Each dimension file should be 500-1000 words
5. Each core file should be 300-500 words

## Reference Materials

- `data/mock_expert_input/` — mock expert reasoning files (if available)
- `docs/SPEC.md` — product spec with tone and content rules
- `docs/ARCHITECTURE.md` — scoring formulas and technical details

## Quality Target

- Generate 5+ profiles with current mock KB
- Expert reviews AI output alongside real lá số data
- Rate each output 1-10
- Target: >= 7/10 average before production
