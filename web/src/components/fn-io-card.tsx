import { LLMJsonCard } from "./llm-json-card";
import { Card, CardContent } from "./ui/card";
import { Label } from "./ui/label";
import { ScrollArea } from "./ui/scroll-area";

interface FunctionIOCardProps {
  labelTitle: string;
  data?: string | Record<string, unknown>;
  errorInfo?: string;
}
/**
 * Tracked function input or output card
 * The component renders input or output as a card
 * 
 * @example
 * ```tsx
 * const data = {foo: "bar"}
 * <FunctionIOCard data={data} labelTitle="input" errorInfo="Errors" />
 * ```
 */
export function FunctionIOCard({
  labelTitle,
  data,
  errorInfo,
}: FunctionIOCardProps) {
  return (
    <div className="flex flex-col flex-1 gap-4">
      {data && typeof data === "string" ? (
        <>
          <Label>{labelTitle}</Label>
          <Card>
            <CardContent>
              <ScrollArea className="max-h-58 overflow-auto rounded-md">
                <pre className="text-sm font-mono whitespace-pre-wrap wrap-break-words text-left">
                  <code>
                    {JSON.stringify(
                      data ? data : errorInfo ?? "Something errors.",
                      null,
                      2
                    )}
                  </code>
                </pre>
              </ScrollArea>
            </CardContent>
          </Card>
        </>
      ) : (
        <LLMJsonCard
          labelTitle="Step Final Output"
          jsonObject={data as Record<string, undefined>}
          errorInfo={errorInfo}
          llmJsonLight={false}
        />
      )}
    </div>
  );
}
