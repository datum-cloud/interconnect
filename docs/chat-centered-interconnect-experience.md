# Interconnect should be a conversation, not a console

**Status:** Proposed
**Scope:** The consumer-facing Interconnect experience. Chat is the primary
surface, with a recommendations rail alongside it. No change to how
interconnects themselves are modeled or provisioned.

## Summary

Instead of building Interconnect around a traditional list-and-forms
console — a table of connections, a "create" wizard, a settings page — we
build it around a conversation with Patch. A customer opens Interconnect
and lands in a conversation, not a dashboard. Alongside it, a
recommendations rail shows the specific interconnect locations most
relevant to that customer.

The two halves reinforce each other: chat for "what should I do and why,"
the rail for "here's exactly where to do it." The bet is that for a product
where the hard part is *deciding*, a conversation that can ask clarifying
questions and reason over the customer's real footprint beats a form that
assumes they already know the answer.

## Why chat-first

Interconnect is a product most customers don't have a mental model for.
Unlike compute or storage, "which physical location should I connect at,
and why" isn't a question most people can answer for themselves — it
depends on where their workloads run, what latency they need, which
carriers and cloud on-ramps they can reach, what's physically available
near them, and what it costs.

A forms-first console fails in three specific ways:

- **The empty state is a dead end.** A table with zero rows and a "Create"
  button tells a first-time customer nothing about what to create.
- **The vocabulary gap is the real blocker.** The customer's problem is "my
  app in Dallas feels slow to customers on the east coast." The form wants
  a facility, a port speed, a VLAN, and a peer ASN. Somebody does that
  translation, and today that somebody is a solutions engineer on a call.
- **The interesting decisions aren't fields.** One site or two, size for
  today or next year, whether the nearest facility is actually the right
  one — none of that is a form input. It's a conversation, and today it
  happens off-platform.

Chat-first flips the order: the customer describes their problem in plain
language, Patch does the translation, and the form — when we need one —
comes pre-filled at the *end* of the conversation rather than blocking its
start.

## Goals

- A customer who arrives knowing nothing about interconnects can leave with
  a specific, actionable decision, without a call.
- Answers are grounded in the customer's actual project — where their
  workloads run, what they already have — not generic advice.
- The customer can always see and act on concrete options, not just read
  about them.
- Day-2 questions ("why is this link slow?") land in the same place as
  day-1 questions, with no separate tool to find.

## Non-Goals

- Replacing the eventual self-service console. Routine paths will earn
  dedicated views; this is about the deciding, not the clicking.
- Having Patch provision anything without an explicit confirmation step.
- Making chat the only way to do things. Anything Patch can do should be
  reachable by clicking something visible.
- Serving the expert who already knows exactly what they want and just
  wants to order it — that customer is better served by the dedicated
  views this experience will eventually graduate.

## Principles

These break the tie when a later decision is ambiguous.

1. **Chat is the entry point, never the only exit.** It resolves ambiguity;
   it is not a command line hiding capability behind magic words.
2. **Every claim about the customer's environment is traceable to a read.**
   Not a plausible guess, and the attribution should be visible.
3. **Patch proposes; the customer disposes.** Reads happen freely. Anything
   that provisions, changes, or costs money is a reviewable proposal.
4. **Say "I don't know" out loud.** A wrong interconnect decision is
   measured in months and circuits, not in an undo.
5. **The rail is the durable artifact.** Conversation scrolls away; the
   narrowed candidate set stays on screen.
6. **Degrade to the boring path.** Chat being unavailable must never mean
   Interconnect is unavailable.

## How it works

The page has three regions: project navigation on the left (Interconnect is
a first-class destination, not a bolted-on app), chat with Patch in the
middle, and the recommendations rail on the right.

Chat is where *reasoning* happens — "you're running in Dallas and Chicago,
so here's what I'd suggest and why." The rail is where the customer
*browses and compares* on their own, without asking Patch to repeat itself.
Chat history persists per project, so a decision made last week is still
readable this week.

### The two surfaces stay in sync

They aren't independent widgets sharing a page; they're two views of the
same working set, coupled both ways.

- **Chat narrows the rail.** "Only the west coast" or "I need 100G"
  re-scopes the candidate set, with a visible note about what filter is
  applied and a one-click way to clear it.
- **The rail seeds chat.** Each card offers a way into the conversation —
  "why this one?", "compare with Ashburn", "what would this cost?" — so the
  customer can go deeper without composing a prompt from scratch.
- **Chat's recommendations are the rail's cards.** When Patch recommends a
  location in prose, it means a card the customer can see. No orphan
  advice.
- **The rail survives a new chat.** Its state belongs to the project, not
  the thread.

### What a recommendation card says

The card is the densest surface in the product, so each field earns its
place. A good card answers "should I look harder at this one?" in three
seconds.

- **Location** — human name plus airport-style code (`Dallas (DFW)`),
  because that's how the industry actually refers to facilities.
- **Proximity to the customer's own footprint** — not abstract latency, but
  latency from where their workloads already run. This is what makes the
  recommendation personal rather than generic.
- **Available capacity** — port speeds actually obtainable there. Picking a
  facility and then discovering 100G isn't available is the worst outcome.
- **Why this is here** — the provenance line that makes the recommendation
  auditable: "closest to your Dallas workloads," "only site in this region
  with 100G." This is principle 2 as product surface, and it's the field
  most likely to get dropped under deadline pressure. It shouldn't be.

Deliberately not on the card: anything requiring the customer to already
speak the product's language. Cross-connect specifics, peer ASNs, and VLAN
details belong in the detail view or the conversation, not the
scan-and-compare surface.

## What Patch can do for the customer

Each step up this gradient carries more risk and needs more consent.

- **Read the project** — where workloads run, what interconnects exist,
  what state they're in. This is the floor; without it, chat is a search
  box over documentation. It's the difference between "connect somewhere
  near your workloads" and "your workload is in Dallas, one replica,
  healthy — here's what that implies."
- **Read the catalog** — facilities, metros, port speeds, reachable
  carriers and cloud on-ramps. Turns a general suggestion into an
  actionable card.
- **Reason and recommend** — compare candidates, weigh trade-offs, and say
  plainly when the difference doesn't matter.
- **Diagnose** — why a link is degraded, what changed, what to check. The
  highest-frequency reason customers come back after setup.
- **Draft a change** — assemble the concrete request as a proposal. Patch
  fills in the form; the customer signs it.
- **Act, on confirmation** — provision only after an explicit yes, with the
  result reported back in the transcript as a durable record.

## What a first session looks like

1. A customer opens Interconnect for the first time and sees a conversation
   inviting them in, with a few starting questions offered. The rail is
   already populated based on where their workloads run — the page is never
   blank.
2. They ask "where should I connect given where my workloads run?" Patch
   answers against their real footprint: "your workloads are in Dallas and
   Ashburn — you'd benefit most from a connection near one of those."
3. The rail already shows those candidates, so they can compare
   immediately rather than waiting for a link or follow-up.
4. They keep going — "why not Chicago?", "do I need two for redundancy?" —
   or act on a card directly.
5. When ready, Patch drafts the request pre-filled. The customer reviews
   and confirms. The reasoning stays in the transcript, which matters when
   someone asks "why did we pick Dallas?" six months later.

Two other shapes matter. **Day two** is diagnostic — "why is my Ashburn
link slow?" — and lands in the same place, with Patch distinguishing what it
*knows* from what it's *inferring*. **Ongoing review** is a question no
dashboard answers: "we just opened a Frankfurt region, does that change
anything?" There the rail shifts from discovery to comparison, showing
candidates against what already exists.

## Risks and mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Customers don't trust an assistant for an expensive, slow-to-reverse decision | Chat becomes decoration; everyone still calls a solutions engineer | Ground every environment claim in a real read, show the footprint reasoned from, distinguish fact from judgment, keep a human escalation path visible |
| Patch asserts something wrong about the customer's environment | Wrong siting decision, unwound over months and circuits rather than with an undo | Make the premises visible so a wrong one is caught before the conclusion is acted on; explicit confirmation before anything provisions |
| Chat is slow or unavailable | Interconnect appears down | Rail and existing connections stay browsable and actionable independent of chat |
| Customer doesn't know what to ask | Bounce on first session — the same dead end as the empty table | Starter prompts, a pre-populated rail, and per-card affordances that open a conversation without composing a prompt |
| Capability is only discoverable by guessing the right phrasing | Customers never find what Patch can do | Everything reachable by clicking something visible; chat is never the only exit |
| The two surfaces drift apart | Customer can't tell whether the rail reflects the conversation they just had | Visible filter state with one-click clear; prose recommendations always refer to cards on screen |

## How we'll know it's working

- **First-session completion** — does a customer who arrives knowing
  nothing leave with an actionable decision, without a call?
- **Return-to-chat rate** — do they come back for day-2 questions, or use
  it once and avoid it? Avoidance after first use is the strongest possible
  signal the answers aren't trusted.
- **Rail vs. chat engagement** — if nobody touches the rail it's
  decoration; if nobody types we've built a dashboard with a chat box
  stapled on. Both halves should get used.
- **Correction rate** — how often a customer has to tell Patch it got their
  environment wrong. The grounding principle, measured.
- **Escalation rate** — and whether escalations happen at genuinely hard
  questions or at ones Patch should have handled.

## Open questions

- Where does the rail get its candidates before the customer says anything?
  Proximity to existing workloads is the obvious default, but a customer
  with workloads in eight regions needs a different heuristic than one with
  workloads in one.
- How much does Patch ask versus assume? A clarifying question is cheap for
  a customer who knows the answer and expensive for one who doesn't. The
  likely default — assume, state the assumption visibly, make it easy to
  correct — is worth testing.
- How do multi-site topologies show up? Redundancy is a recommendation
  about a *set*, not a list of individual cards. The current card model
  doesn't express that.
- What's the right unit of persistence for the narrowed candidate set —
  project, user, or conversation?
- How does this serve a customer with an existing, healthy footprint?
  Discovery framing suits the newcomer; someone arriving with a specific
  operational question shouldn't have to scroll past it.

## Alternatives considered

- **A traditional list-and-forms console**: rejected for the three failure
  modes above — the dead-end empty state, the vocabulary gap, and the fact
  that the decisions that actually matter aren't form fields. This remains
  the right shape for routine paths later, once customers know what they
  want.
- **Chat alone, with no rail**: rejected because conversation scrolls away.
  The customer would have to re-ask to compare options, and there'd be
  nothing to click — capability discoverable only by guessing the right
  phrasing.
- **A dashboard with a docked chat helper**: rejected because it relegates
  reasoning to a support afterthought. For this product the deciding *is*
  the main task, so it gets the main surface.
- **A guided wizard or questionnaire instead of open conversation**:
  rejected because a fixed question order can't adapt to what the customer
  already knows, and it still forces them to translate their problem into
  the product's vocabulary before it can help.
