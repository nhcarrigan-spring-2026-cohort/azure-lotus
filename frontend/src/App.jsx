import { Routes, Route } from "react-router-dom"
import Navbar from "./components/Navbar.jsx"
import Home from "./pages/Home.jsx"
import About from "./pages/about.jsx"
import Explained from "./pages/explained.jsx"
import Signup from "./pages/signup.jsx"

export default function App() {
  return (
    <>

      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/explained" element={<Explained />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>

    </>
  )
}
