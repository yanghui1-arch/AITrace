import type { ReactElement } from "react";

interface LLMJsonHighlightProps {
  jsonObject: Record<string, unknown>;
}

export function LLMJsonHighlight({ jsonObject }: LLMJsonHighlightProps) {
  return (
    <span className="font-mono text-sm">
      {"{"}
      {Object.entries(jsonObject).map(([key, value], idx, arr) => (
        <div key={key} className="ml-4">
          <span className="foreground">"{key}"</span>
          <span className="foreground">: </span>
          {renderValue(value, key)}
          {idx < arr.length - 1 && <span>,</span>}
        </div>
      ))}
      {"}"}
    </span>
  );
}

/**
 * 根据值类型（对象/数组/基本类型）进行渲染
 */
function renderValue(value: unknown, keyName?: string): ReactElement {
  if (value === null) {
    return <span className="foreground">null</span>;
  }

  if (Array.isArray(value)) {
    return (
      <span>
        [<br />
        {value.map((item, i) => (
          <div key={i} className="ml-4">
            {typeof item === "object" && item !== null ? (
              // if item type is object and include role and one of `content`, `audio` or `tool_calls` (think it as llm parmeters)
              "role" in item &&
              ["content", "audio", "tool_calls"].some((k) => k in item) ? (
                <div
                  className={`rounded-md ${
                    (item as any).role === "user"
                      ? "bg-json-1"
                      : (item as any).role === "assistant"
                      ? "bg-json-2"
                      : (item as any).role === "tool"
                      ? "bg-json-3"
                      : "bg-json-4"
                  }`}
                >
                  <LLMJsonHighlight jsonObject={item as Record<string, unknown>} />
                </div>
              ) : (
                <LLMJsonHighlight jsonObject={item as Record<string, unknown>} />
              )
            ) : (
              <span className="text-amber-400">{String(item)}</span>
            )}
            {i < value.length - 1 && <span className="text-gray-400">,</span>}
          </div>
        ))}
        ]
      </span>
    );
  }

  if (typeof value === "object") {
    return <LLMJsonHighlight jsonObject={value as Record<string, unknown>} />;
  }

  if (typeof value === "string") {
    return <span>
      "{value}"
    </span>
  }

  return (
    <span
    >
      {String(value)}
    </span>
  );
}
