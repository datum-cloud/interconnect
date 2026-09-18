import { AssistantWorkspace } from '@datum-cloud/datum-ui/assistant';
import { usePluginFetch, useProjectContext } from '@datum-cloud/portal-plugin-sdk';
import { useAssistantWorkspace } from '@datum-cloud/assistant-chat-kit';

import { ASSISTANT_CONFIG } from '../lib/assistant-config';

/**
 * `Assistant` — the module exposed as `interconnect.datumapis.com/Assistant`,
 * `$codeRef`'d by the `portal.page/project` extension in
 * `public/plugin-manifest.json` (routed at `.../services/interconnect/assistant`).
 *
 * Full-page counterpart to the assistant plugin's docked `ChatDock`: same
 * conversation logic (`@datum-cloud/assistant-chat-kit`'s
 * `useAssistantWorkspace`, talking to the same per-project Patch backend —
 * interconnect-specific answers come from that backend's own `AgentBinding`
 * capability document, not from anything here), same presentational shell
 * (`@datum-cloud/datum-ui/assistant`'s `AssistantWorkspace`), just laid out to
 * fill a routed page instead of a docked panel.
 *
 * Reads its host wiring from `@datum-cloud/portal-plugin-sdk`'s
 * `usePluginFetch()`/`useProjectContext()` rather than props, same reason as
 * `ChatDock`: a Module Federation `$codeRef` is mounted generically by the
 * host with no way to pass props in.
 */
export default function Assistant() {
  const { project } = useProjectContext();
  const pluginFetch = usePluginFetch();
  const projectName = project?.name ?? '';
  const workspace = useAssistantWorkspace({ pluginFetch, projectName });

  return (
    <div
      data-testid="interconnect-assistant-page"
      aria-label="Patch AI"
      style={{ position: 'relative', height: '100%', width: '100%' }}
    >
      <AssistantWorkspace
        config={ASSISTANT_CONFIG}
        title={workspace.title}
        messages={workspace.messages}
        status={workspace.status}
        error={workspace.error}
        isReady={workspace.isReady}
        chatList={workspace.chatList}
        currentChatId={workspace.currentChatId}
        sidebarHeader={
          project ? (
            <div style={{ minWidth: 0 }}>
              <p style={{ opacity: 0.5, fontSize: '0.7rem' }}>Project</p>
              <p style={{ fontSize: '0.75rem', fontWeight: 500 }}>
                {project.displayName ?? project.name}
              </p>
            </div>
          ) : undefined
        }
        editor={workspace.editor}
        htmlByUserMsgIndex={workspace.htmlByUserMsgIndex}
        bottomRef={workspace.bottomRef}
        containerRef={workspace.containerRef}
        userScrolledUpRef={workspace.userScrolledUpRef}
        onSend={workspace.onSend}
        onStop={workspace.onStop}
        onRetry={workspace.onRetry}
        onNewChat={workspace.onNewChat}
        onLoadChat={workspace.onLoadChat}
        onArchiveChat={workspace.onArchiveChat}
        onUnarchiveChat={workspace.onUnarchiveChat}
        onDeleteChat={workspace.onDeleteChat}
        confirmDelete
        onSuggestion={workspace.onSuggestion}
        modelId={workspace.modelId}
        effortId={workspace.effortId}
        onModelChange={workspace.onModelChange}
        onEffortChange={workspace.onEffortChange}
        micSupported={workspace.micSupported}
        micListening={workspace.micListening}
        micFrequencyData={workspace.micFrequencyData}
        onMicToggle={workspace.onMicToggle}
        historyOpen={workspace.historyOpen}
        onToggleHistory={workspace.onToggleHistory}
      />
      {workspace.error && workspace.messages.length === 0 && (
        <p
          role="alert"
          style={{ position: 'absolute', top: 0, left: 0, right: 0, padding: '0.5rem', textAlign: 'center', fontSize: '0.75rem', color: 'var(--destructive, #dc2626)' }}
        >
          {workspace.error.message}
        </p>
      )}
      {!project && (
        <p role="status" style={{ position: 'absolute', bottom: 0, left: 0, right: 0, opacity: 0.7 }}>
          No project context supplied — running with an empty project scope.
        </p>
      )}
    </div>
  );
}
