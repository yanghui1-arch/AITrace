import { DataTable } from "@/components/data-table";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import axios from "axios";
import { stepColumns, type Step } from "./step-columns";
import { Separator } from "@/components/ui/separator";
import { RowPanelContent } from "@/components/data-table/data-table-row-panel";
import { Label } from "@/components/ui/label";
import TokensPanel from "@/components/tokens-panel";
import { Card, CardContent } from "@/components/ui/card";
import { Clock } from "lucide-react";
import { StepDetail } from "@/components/step-details";

export default function ProjectDetailPage() {
  const { name } = useParams<{ name: string }>();
  const location = useLocation();
  const projectDescription = location.state.description;

  const [navButtonType, setNavButtonType] = useState<
    "step" | "trace" | "conversation"
  >("step");
  const isNavButtonDisabled = (buttonType: string) => {
    return navButtonType === buttonType;
  };

  const [stepData, setStepData] = useState<Step[]>([]);

  useEffect(() => {
    const api = axios.create({
      baseURL: "/api/v0",
      timeout: 5000,
    });

    api.interceptors.response.use(
      (res) => res.data,
      (err) => {
        console.error(err);
        return Promise.reject(err);
      }
    );

    const loadStepDataOfProject = async () => {
      const steps = await api.get(
        `/step/${encodeURIComponent("aitrace_demo")}`
      );
      setStepData(steps.data);
    };
    loadStepDataOfProject();
  }, []);

  return (
    <div className="flex flex-col gap-2 px-4 lg:px-6">
      <h2 className="text-xl font-semibold">{name}</h2>
      <p className="text-muted-foreground mt-2 truncate">
        {projectDescription}
      </p>
      <div className="mt-4">
        <Link to="/projects" className="underline">
          Back to Projects
        </Link>
      </div>
      <div className="flex gap-4 py-2">
        <Button
          variant="link"
          className={isNavButtonDisabled("step") ? "bg-white text-black" : ""}
          onClick={() => {
            if (isNavButtonDisabled("step")) {
              return;
            }
            setNavButtonType("step");
          }}
        >
          Step
        </Button>
        <Button
          variant="link"
          className={isNavButtonDisabled("trace") ? "bg-white text-black" : ""}
          onClick={() => {
            if (isNavButtonDisabled("trace")) {
              return;
            }
            setNavButtonType("trace");
          }}
        >
          Trace
        </Button>
        <Button
          variant="link"
          className={
            isNavButtonDisabled("conversation") ? "bg-white text-black" : ""
          }
          onClick={() => {
            if (isNavButtonDisabled("conversation")) {
              return;
            }
            setNavButtonType("conversation");
          }}
        >
          Conversation
        </Button>
      </div>
      <Separator />
      <div className="container mx-auto py-2">
        <DataTable data={stepData} columns={stepColumns}>
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
                                      : rowData.errorInfo ??
                                          "Something errors.",
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
                        <StepDetail labelTitle="Input" jsonObject={rowData.input.llm_inputs as Record<string, unknown>} />
                      </div>
                      <div className="h-full border-l border-muted" />
                      <div className="flex flex-col flex-1 gap-4 w-full">
                        <StepDetail labelTitle="Output" jsonObject={rowData.output.llm_outputs as unknown as Record<string, unknown>} errorInfo={rowData.errorInfo} llmJsonLight={true}/>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </RowPanelContent>
        </DataTable>
      </div>
    </div>
  );
}
