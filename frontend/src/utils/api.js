import axios from "axios";
import config from "../core/config";

const apiURL = config.API_BASE_URL;

export const login = async (email, password) => {
  try {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);
    formData.append("grant_type", "password");

    const response = await axios.post(`${apiURL}/auth/jwt/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  } catch (error) {
    if (error.response && error.response.data) {
      return { success: false, message: error.response.data.detail };
    }
    return { success: false, message: "Login failed." };
  }
};

export const register = async (email, password) => {
  try {
    const response = await axios.post(`${apiURL}/auth/register`, {
      email,
      password,
    });
    if (response.status === 201) {
      return { success: true, data: response.data };
    }
    return { success: false, message: 'Registration failed.' };
  } catch (error) {
    if (error.response && error.response.data) {
      return { success: false, message: error.response.data.detail };
    }
    return { success: false, message: 'Registration failed.' };
  }
};


export const verifyToken = async (token) => {
  try {
    const response = await axios.post(`${apiURL}/auth/verify`, { token }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    if (error.response && error.response.data) {
      throw new Error(error.response.data.detail);
    }
    throw new Error("Token verification failed due to a server error.");
  }
};

export const logout = async (token) => {
  try {
    const response = await axios.post(`${apiURL}/auth/jwt/logout`, {}, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    if (error.response && error.response.data) {
      throw new Error(error.response.data.detail);
    }
    throw new Error("Logout failed due to a server error.");
  }
};
