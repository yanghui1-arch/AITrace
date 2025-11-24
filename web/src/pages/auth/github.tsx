import { authApi } from "@/api/auth";
import { Label } from "@/components/ui/label";
import { LoaderCircleIcon } from "lucide-react";
import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { toast } from "sonner";

const GITHUB_CODE_FLAG = "github_auth_code_handled";

export default function GitHubAuthPage() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  useEffect(() => {
    const githubCode = searchParams.get("code");

    if (!githubCode) {
      return;
    }
    const handledCode = sessionStorage.getItem(GITHUB_CODE_FLAG);

    if (handledCode === githubCode) {
      return;
    }

    sessionStorage.setItem(GITHUB_CODE_FLAG, githubCode);
    authApi
      .authenticate(githubCode)
      .then((res) => {
        const { code, message } = res.data;
        console.log(code)
        if (code === 200) {
          toast.success("Welcome to AITrace!");
          setSearchParams({}, { replace: true });
          navigate("/overview", { replace: true });
        } else {
          toast.error("Failed to authentication with GitHub", {
            description: message ?? "Unexpected error",
          });
        }
      })
      .catch((error) => {
        sessionStorage.removeItem(GITHUB_CODE_FLAG);
        console.error("GitHub authenticate error:", error);
        const msg =
          (error.response && error.response.data?.message) ||
          error.message ||
          "Network error";
        toast.error("Failed to authentication with GitHub", {
          description: msg,
        });
      });
  }, [searchParams, navigate, setSearchParams]);
  return (
    <div className="h-screen flex items-center justify-center">
      <Label className="font-semibold">
        <LoaderCircleIcon className="animate-spin" />
        Loading
      </Label>
    </div>
  );
}
