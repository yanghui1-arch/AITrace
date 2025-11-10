import { type Step } from "@/pages/projects/track/step-columns";
import { DataTable } from "./data-table";
import { RowPanelContent } from "./data-table/data-table-row-panel";
import { Clock } from "lucide-react";
import TokensPanel from "./tokens-panel";
import { Separator } from "@radix-ui/react-separator";
import { Label } from "./ui/label";
import { StepDetail } from "./step-details";
import { Card, CardContent } from "./ui/card";
import type { ColumnDef } from "@tanstack/react-table";

interface StepTableProps<TValue> {
  columns: ColumnDef<Step, TValue>[];
  data: Step[];
}

export function StepTable<TValue>({ columns, data }: StepTableProps<TValue>) {
  return (
    <div className="container mx-auto py-2">
      <DataTable data={data} columns={columns}>
        <RowPanelContent<Step>>
          {(rowData) => (
            <div className="flex gap-4 flex-col">
              <div className="ml-auto font-mono text-xs flex gap-1">
                <Clock size={"16px"} />
                {new Date(rowData.endTime).getTime() -
                  new Date(rowData.startTime).getTime() <
                1000
                  ? new Date(rowData.endTime).getTime() -
                    new Date(rowData.startTime).getTime() +
                    "ms"
                  : (
                      (new Date(rowData.endTime).getTime() -
                        new Date(rowData.startTime).getTime()) /
                      1000
                    ).toFixed(2) + "s"}
              </div>
              <TokensPanel
                model={rowData.model}
                usage={rowData.usage}
                cost={1}
              />
              <Separator />
              <Label className="font-semibold">Step Function Details</Label>
              {rowData.input.func_inputs && (
                <div className="flex gap-4">
                  <div className="flex flex-col flex-1 gap-4">
                    <StepDetail
                      labelTitle="Step Original Input"
                      jsonObject={rowData.input.func_inputs}
                    />
                  </div>
                  <div className="h-full border-l-5 border-muted" />
                  <div className="flex flex-col flex-1 gap-4">
                    {rowData.output.func_output &&
                    typeof rowData.output.func_output === "string" ? (
                      <>
                        <Label>Step Final Output</Label>
                        <Card>
                          <CardContent>
                            <pre className="text-sm font-mono whitespace-pre-wrap wrap-break-words text-left">
                              <code>
                                {JSON.stringify(
                                  rowData.output.func_output
                                    ? rowData.output.func_output
                                    : rowData.errorInfo ?? "Something errors.",
                                  null,
                                  2
                                )}
                              </code>
                            </pre>
                          </CardContent>
                        </Card>
                      </>
                    ) : (
                      <StepDetail
                        labelTitle="Step Final Output"
                        jsonObject={
                          rowData.output.func_output as Record<
                            string,
                            undefined
                          >
                        }
                        errorInfo={rowData.errorInfo}
                        llmJsonLight={false}
                      />
                    )}
                  </div>
                </div>
              )}
              <Separator />
              <Label className="font-semibold">LLM Details</Label>
              <div className="flex flex-col gap-4">
                {rowData.input.llm_inputs && (
                  <div className="flex gap-4">
                    <div className="flex flex-col flex-1 gap-4">
                      <StepDetail
                        labelTitle="Input"
                        jsonObject={
                          rowData.input.llm_inputs as Record<string, unknown>
                        }
                      />
                    </div>
                    <div className="h-full border-l border-muted" />
                    <div className="flex flex-col flex-1 gap-4 w-full">
                      <StepDetail
                        labelTitle="Output"
                        jsonObject={
                          rowData.output.llm_outputs as unknown as Record<
                            string,
                            unknown
                          >
                        }
                        errorInfo={rowData.errorInfo}
                        llmJsonLight={true}
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </RowPanelContent>
      </DataTable>
    </div>
  );
}
