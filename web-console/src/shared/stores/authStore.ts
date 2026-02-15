import { create } from 'zustand';

interface User {
    id: string;
    username: string;
    name: string;
}

interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (credentials: { username: string; password: string }) => Promise<void>;
    logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    login: async ({ username, password }) => {
        set({ isLoading: true });
        // Mock API call
        await new Promise((resolve) => setTimeout(resolve, 800));

        if (username === 'admin' && password === 'admin') {
            set({
                user: { id: '1', username, name: '管理员' },
                isAuthenticated: true,
                isLoading: false
            });
        } else {
            set({ isLoading: false });
            throw new Error('用户名或密码错误');
        }
    },
    logout: () => set({ user: null, isAuthenticated: false }),
}));
