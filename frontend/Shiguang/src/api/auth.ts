import {jwtDecode} from 'jwt-decode'

export interface JWTPayload {
  exp: number; // 过期时间戳
  iat: number; // 签发时间
  [key: string]: any;
}

const ACCESS_TOKEN_KEY = 'token'
const REFRESH_TOKEN_KEY = 'refresh'

export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY)
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY)
}

export function setTokens(access: string, refresh?: string) {
  localStorage.setItem(ACCESS_TOKEN_KEY, access)
  if (refresh) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
  }
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

export function isTokenExpired(token: string | null): boolean {
  if (!token) return true
  try {
    const decoded: JWTPayload = jwtDecode(token)
    return decoded.exp * 1000 < Date.now()
  } catch {
    return true
  }
}

export function isLoggedIn(): boolean {
  const token = getAccessToken()
  return !!token && !isTokenExpired(token)
}
