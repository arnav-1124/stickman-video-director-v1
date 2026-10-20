# Mandatory Rule: Skill Pre-Flight & Autonomous Discovery Protocol

## Directive
**FOR EVERY AGENT SESSION AND FOR EVERY PROMPT**:
Before formulating a plan, writing code, executing pipeline commands, or generating video/creative assets, the agent **MUST** actively inspect and read the relevant specialized skills (`.agents/skills/<skill-name>/SKILL.md` or global skills).

## Execution Protocol
1. **Analyze Prompt Intent**:
   - Identify domain areas triggered by the user's request (e.g. 2D character rigging, Three.js 3D rendering, Remotion composition, audio mastering, GSAP animation, prompt engineering, retention auditing).
2. **Scan Available Skills**:
   - Cross-reference the intent with available skills in `.agents/skills/` and global environment skills.
3. **Mandatory Reading Before Action**:
   - Call `view_file` on each matching `SKILL.md` before generating code or taking action.
   - Never assume or guess implementation details when a dedicated skill exists.
4. **Adhere to Skill Constraints & Best Practices**:
   - Enforce the architecture, performance rules, schemas, and best practices documented in the loaded skill.
5. **Transparency**:
   - Explicitly note in thoughts and action summaries which skill(s) were consulted to ensure auditable compliance.
