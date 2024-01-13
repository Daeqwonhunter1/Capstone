import axios from "axios"

export const loadUsers = async () => {
    const res = await axios.get("http://localhost:8080/users")
    console.log(res.data)
}