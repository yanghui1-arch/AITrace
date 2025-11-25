import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { IconKey } from "@tabler/icons-react";

export function APIKeyPage() {
  const apikey = "xxxx";
  return (
    <div className="flex flex-col gap-4 px-4 lg:px-6">
      <h2 className="text-xl font-semibold">Get your AITrace API key</h2>
      <div className="flex gap-2 w-[50%]">
        <div className="flex gap-2 h-9 items-center rounded-md border border-input bg-background px-3 text-sm w-[50%]">
          <IconKey />
          <span className="text-muted-foreground truncate">{apikey}</span>
        </div>
        <div className="flex flex-col gap-2">
          <Button variant="outline">
            <Label>Check your API key</Label>
          </Button>
          <Button variant="outline">
            <Label>Change another</Label>
          </Button>
        </div>
      </div>
    </div>
  );
}
