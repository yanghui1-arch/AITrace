import { useState } from "react";
import { userProviderContext, type User } from "./use-user";

type UserProviderProps = {
  children: React.ReactNode;
};

export function UserProvider({ children }: UserProviderProps) {
  const [user, setUser] = useState<User | null>(null);

  return (
    <userProviderContext.Provider value={{ user, setUser }}>
      {children}
    </userProviderContext.Provider>
  );
}
