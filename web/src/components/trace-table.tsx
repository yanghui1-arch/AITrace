import type { Trace } from "@/pages/projects/track/trace-columns";
import { DataTable } from "./data-table";
import { RowPanelContent } from "./data-table/data-table-row-panel";
import type { ColumnDef } from "@tanstack/react-table";
import { Clock } from "lucide-react";
import TokensPanel from "./tokens-panel";
import type { CompletionUsage } from "openai/resources/completions.mjs";
import { TraceDialogMain } from "./trace-dialog/trace-dialog-main";
import { useDataTable } from "@/hooks/use-datatable";
import { DataTableToolbar } from "./data-table/data-table-toolbar/common-data-table-toolbar";

interface TraceTableProps<TValue> {
  columns: ColumnDef<Trace, TValue>[];
  data: Trace[];
}

export function TraceTable<TValue>({ columns, data }: TraceTableProps<TValue>) {

  const { table } = useDataTable({ columns, data })

  return (
    <div className="container mx-auto py-2 space-y-4">
      <DataTableToolbar table={table}/>
      <DataTable table={table}>
        <RowPanelContent<Trace>>
          {(rowData) => {
            /* generate a new grouping result based model name and don't udpate rowData.tracks */
            const groupedUsage = rowData.tracks.reduce(
              (acc, track) => {
                const model: string | undefined = track.step.model;
                const usage: CompletionUsage | undefined = track.step.usage;
                if (!usage || !model) return acc;

                const prev = acc.get(model);
                if (prev) {
                  /* create a copy */
                  const newUsage = { ...prev };

                  /* merge token usage */
                  const addUsage = (preToken?: number, curToken?: number): number | undefined => {
                    return preToken === undefined || curToken === undefined ? undefined : preToken + curToken
                  }
                  const mergeCompletionTokensDetails = (
                    preCompletionTokensDetails?: CompletionUsage.CompletionTokensDetails, 
                    curCompletionTokensDetails?: CompletionUsage.CompletionTokensDetails
                  ): CompletionUsage.CompletionTokensDetails | undefined => {

                    return preCompletionTokensDetails === undefined || curCompletionTokensDetails == undefined ? undefined : (
                      {
                        accepted_prediction_tokens: addUsage(preCompletionTokensDetails.accepted_prediction_tokens, curCompletionTokensDetails.accepted_prediction_tokens),
                        audio_tokens: addUsage(preCompletionTokensDetails.audio_tokens, curCompletionTokensDetails.audio_tokens),
                        reasoning_tokens: addUsage(preCompletionTokensDetails.reasoning_tokens, curCompletionTokensDetails.reasoning_tokens),
                        rejected_prediction_tokens: addUsage(preCompletionTokensDetails.rejected_prediction_tokens, curCompletionTokensDetails.rejected_prediction_tokens),
                      }
                    )
                  }
                  const mergePromptTokensDetails = (
                    prePromptTokensDetails?: CompletionUsage.PromptTokensDetails,
                    curPromptTokensDetails?: CompletionUsage.PromptTokensDetails,
                  ): CompletionUsage.PromptTokensDetails | undefined => {
                    return prePromptTokensDetails === undefined || curPromptTokensDetails === undefined ? undefined : (
                      {
                        audio_tokens: addUsage(prePromptTokensDetails.audio_tokens, curPromptTokensDetails.audio_tokens),
                        cached_tokens: addUsage(prePromptTokensDetails.cached_tokens, curPromptTokensDetails.cached_tokens),
                      }
                    )
                  }

                  newUsage.completion_tokens += usage.completion_tokens;
                  newUsage.prompt_tokens += usage.prompt_tokens;
                  newUsage.total_tokens += usage.total_tokens;
                  newUsage.completion_tokens_details = mergeCompletionTokensDetails(newUsage.completion_tokens_details, usage.completion_tokens_details);
                  newUsage.prompt_tokens_details = mergePromptTokensDetails(newUsage.prompt_tokens_details, usage.prompt_tokens_details);
                  
                  acc.set(model, newUsage);
                } else {
                  acc.set(model, { ...usage });
                }

                return acc;
              },
              new Map<string, CompletionUsage>()
            );

            return (
              <div className="flex gap-4 flex-col">
                <div className="ml-auto font-mono text-xs flex gap-1">
                  <Clock size={"16px"} />
                  {(() => {
                    const delta =
                      new Date(rowData.lastUpdateTimestamp).getTime() -
                      new Date(rowData.startTime).getTime();
                    return delta < 1000 ? `${delta}ms` : `${(delta / 1000).toFixed(2)}s`;
                  })()}
                </div>
                {Array.from(groupedUsage.entries()).map(([model, completionUsage]) => (
                  <TokensPanel
                    key={model}
                    model={model}
                    usage={completionUsage}
                    cost={1}
                  />
                ))}
                <TraceDialogMain data={rowData}/>
              </div>
            );
          }}
        </RowPanelContent>
      </DataTable>
    </div>
  );
}
