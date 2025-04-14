import { error } from "console";
import { createContext, ReactNode, useContext } from "react";

type LoginType = {
  email: string;
  password: string;
  remember_me?: boolean | undefined;
};

interface AuthContextType {
  user: String | null;
  token: string;
  login(data: LoginType): void;
  logout(): void;
}

const AuthContext = createContext<AuthContextType | undefined>({
  user: null,
  token: "",
  login: () => {},
  logout: () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {}

// Custom Hook
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used with an AuthProvider");
  }
  return context;
}
