import { useEffect, useState } from "react";
import { userProviderContext, type User } from "./use-user";
import { AT_JWT } from "@/types/storage-const";
import { authApi } from "@/api/auth";

type UserProviderProps = {
  children: React.ReactNode;
};

export function UserProvider({ children }: UserProviderProps) {
  const [user, setUser] = useState<User | null>(null);

  const isAtJwtExpired = (atJwt: string) => {
    const payload = JSON.parse(atob(atJwt.split('.')[1]));
    const exp = payload.exp * 1000;
    return Date.now() > exp;
  }

  useEffect(() => {
    const token = localStorage.getItem(AT_JWT);
    if (token && !isAtJwtExpired(token)) {
      const getUserFromJwt = async () => {
        const response = await authApi.me();
        const code = response.data.code;
        if (code === 200) {
          setUser( {userName: response.data.data.userName, avatar: response.data.data.avatar} );
        } else {
          console.error(response.data.message);
        }
      }
      getUserFromJwt();
    }
  }, [])

  return (
    <userProviderContext.Provider value={{ user, setUser }}>
      {children}
    </userProviderContext.Provider>
  );
}
