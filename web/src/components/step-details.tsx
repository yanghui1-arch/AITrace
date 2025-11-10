import { LLMJsonHighlight } from "./json-highlight";
import { Card, CardContent } from "./ui/card";
import { Label } from "./ui/label";
import { ScrollArea } from "./ui/scroll-area";

interface StepDetailProp {
  labelTitle: string;
  jsonObject?: Record<string, unknown>;
  errorInfo?: string;
  llmJsonLight?: boolean;
}

export function StepDetail({
  labelTitle,
  jsonObject,
  errorInfo,
  llmJsonLight = true,
}: StepDetailProp) {
  return (
    <>
      <Label>{labelTitle}</Label>
      <Card>
        <CardContent>
          <ScrollArea className="max-h-58 overflow-auto rounded-md">
            <pre className="text-sm font-mono whitespace-pre-wrap wrap-break-words text-left pr-4">
              <code>
                {jsonObject ? (
                  llmJsonLight ? (
                    <LLMJsonHighlight jsonObject={jsonObject} />
                  ) : (
                    <>{JSON.stringify(jsonObject, null, 2)}</>
                  )
                ) : (
                  errorInfo ? errorInfo : "No content."
                )}
              </code>
            </pre>
          </ScrollArea>
        </CardContent>
      </Card>
    </>
  );
}
