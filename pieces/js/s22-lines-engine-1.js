// =====================================================================
// 22. LINES
// The dialogue engine (Pillar 4, the dialogue engineer, 0.43.x): what crew say, from plain text files writers fill
// under content/ (the writers' guide: content/README.md). content_gen.py bakes them into the generated blocks below;
// nobody hand-edits those. This section sits before section 18 so 18 and 20 can read the baked data at load; its
// own code is lazy (it never touches ROSTER or SHIP at load).
//   lineFor(who, kind, ctx) -> { text, id, kind, tone } | null   who: a person or a crew id; kind: 'greet', 'feel', ...
//     The person's own lines (VOICE[id].lines), then their voice template's, then the shared bank (LINES[kind]);
//     keeps those whose conditions all hold; the most specific wins (own > template > shared, then more conditions);
//     lines said recently lose points (the last 6 by this person in an earlier hour, the last 12 ship-wide by anyone
//     else); a seeded pick by person and hour (schedU k 750), so a second tap in the same hour says the same; fills
//     placeholders ({me}, {room}, {best}...; a line that can't be filled is skipped) and voice tokens ({hi}, {nick}...).
//     A told: line is said once: lineFor calls section 20's memTold. ctx: { t, other, room, thing, trad, machine,
//     dish, deck, act, place, flags, peek } (peek: don't count it as said; flags: { key: true } answers flag: for those keys).
//   overheardFor(a, b, ctx) -> [{ who, text }] | null   a conversation between two crew (CONVOS), A = a, B = b
//   linesOk(e, p, ctx)   does a line's every condition hold (the frozen vocabulary: content/README.md, "Conditions")
//   HOME_CONTACTS / HOME_MOMENTS / HOME_SEND / HOME_CHAT (generated, content/home/*.call) are social B's calls home
//   MOMENTS / MOMENT_THEMES (generated) are social B's moments (content/arcs, content/themes); when: is checked with linesOk
//   TRADITIONS (generated, an array) is the traditions engineer's shape (plans/trad-format.md), read by section 18's loader
//   linesLegacy(kind)    section 20's old lists, from the lines moved into content/banks/old.lines, in their old shapes
// Social conditions read only section 20's pure queries (relTier, mem, warmth, affBand, bondOf, moodOf, beatOf,
// knowsNews, repBand, repShip, knownFor, cue) and section 13's flag; while one isn't there yet, its condition fails
// (and a negated one holds). schedU keys 750-799 are this section's.
