import {Routes, Route} from "react-router"
import Navbar from "./components/Navbar.jsx"
import About from "./pages/about.jsx"
import Explained from "./pages/explained.jsx"
import Home from "./pages/Home.jsx"
import Signup from "./pages/signup.jsx"
import Login from "./pages/Login.jsx"
import {QueryClientProvider} from "@tanstack/react-query";
import {queryClient} from "./lib/query-client.js";
import {AuthProvider} from "./context/AuthContext.jsx";

export default function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <AuthProvider>
                <Navbar/>

                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/about" element={<About/>}/>
                    <Route path="/explained" element={<Explained/>}/>
                    <Route path="/signup" element={<Signup/>}/>
                    <Route path="/login" element={<Login/>}/>
                </Routes>
            </AuthProvider>
        </QueryClientProvider>

    )
}
