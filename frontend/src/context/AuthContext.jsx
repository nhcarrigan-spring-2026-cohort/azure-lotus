import {createContext, useContext, useState} from 'react';
import api from '../lib/axios.js';
import {useMutation} from '@tanstack/react-query';
import {useNavigate} from 'react-router'

const AuthContext = createContext(null);

/* Requests */

// TODO: handle errors
const loginRequest = async ({email, password}) => {
    const {data} = await api.post('/auth/login', {
        email,
        password,
    });
    return data;
};

/**
 * Register: auth/register
 * @param {string} firstname
 * @param {string} lastname
 * @param {string} email
 * @param {string} phoneNumber
 * @param {string} password
 * @typedef {"family" | "volunteer" | "senior"} UserRole
 * @returns {Promise<Object>}
 */
const registerRequest = async ({
    firstname,
    lastname,
    email,
    phoneNumber,
    password,
    role
}) => {
    try {
        const {data} = await api.post('/auth/register', {
            first_name: firstname,
            last_name: lastname,
            email,
            phone_number: phoneNumber,
            password,
            roles: role
        })
        return data
    } catch (e) {
        // TODO: Backend should return more specific error messages
        throw e // rethrow for react query to handle
    }

}

export function AuthProvider({children}) {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [accessToken, setAccessToken] = useState(null);

    let navigate = useNavigate()

    const login = useMutation({
        mutationFn: loginRequest,
        onSuccess: (user) => {
            console.log(`Login successful, ${JSON.stringify(user)}`);
            setIsAuthenticated(true);
            setAccessToken(user.access_token);
            setUser(user.user_info);
            navigate('/')
        },
    });

    const register = useMutation({
        mutationFn: registerRequest,
        onSuccess: (user) => {
            console.log(`Registration successful, ${JSON.stringify(user)}`);
        },
        onError: (error) => {
            // TODO: frontend should show user the error
            console.log(`Registration failed, ${JSON.stringify(error.message)}`);
        }
    })

    const logout = () => {
        // TODO: use backend logout endpoint
        setIsAuthenticated(false);
    };

    const authValue = {
        register,
        login,
        logout,
        user,
        isAuthenticated,
        accessToken
    };

    return (
        <AuthContext.Provider value={authValue}>{children}</AuthContext.Provider>
    );
}

export const useAuthContext = () => {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
    return ctx;
};
