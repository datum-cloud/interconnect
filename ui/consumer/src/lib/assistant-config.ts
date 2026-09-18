import { defaultRenderLink } from '@datum-cloud/datum-ui/assistant';
import type { AssistantConfig } from '@datum-cloud/datum-ui/assistant';

/**
 * This plugin's concrete `AssistantConfig` ("Patch"), mirroring the assistant
 * plugin's own `assistant-config.ts` but with copy specific to interconnect
 * rather than the generic project-scoped defaults — the backend it talks to
 * is the same Patch service, scoped to interconnect tools/skills via that
 * service's own `AgentBinding` capability document.
 */

/** Starter prompts on the empty/new-chat state. */
export const SUGGESTIONS = [
  'What interconnects do I have in this project?',
  'Help me diagnose a degraded interconnect.',
  'What can Patch help me with here?',
] as const;

/**
 * Tool name → progress label shown while a tool call is running. Starts
 * empty, same reasoning as the assistant plugin's own config — this
 * plugin's backend tool set isn't fixed/known ahead of time.
 */
export const TOOL_LABELS: Record<string, string> = {};

export const ASSISTANT_CONFIG: AssistantConfig = {
  greeting: (name) => `Hey there${name ? `, ${name}` : ''}`,
  suggestions: [...SUGGESTIONS],
  // No reasoning-part source on this transport (the apiserver's SSE envelope
  // has no `reasoning`/`thinking` event) — hide the toggle rather than fake it.
  showReasoning: false,
  // No model/effort picker — the server side (a2a runner) chooses the model.
  modelSelector: false,
  toolLabels: TOOL_LABELS,
  renderLink: defaultRenderLink,
};
