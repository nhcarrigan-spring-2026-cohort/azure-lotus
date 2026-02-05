import api from "../lib/axios.js"
import { useMutation } from "@tanstack/react-query"

const loginRequest = async ({username, password}) => {
    const {data} = await api.post("/auth/login", {
        username,
        password
    })
    return data
}

export const useAuth = () => {
    const login = useMutation({
        mutationFn: loginRequest,
        onSuccess: (user) => {
            console.log(`Login successful, ${JSON.stringify(user)}`)
        }
    })

    return {
        login
    }
}