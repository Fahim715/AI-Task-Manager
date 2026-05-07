import { NextResponse } from "next/server";
import { cookies } from "next/headers";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const isProd = process.env.NODE_ENV === "production";

export async function POST() {
  const refreshToken = cookies().get("refresh_token")?.value;
  if (!refreshToken) {
    return NextResponse.json({ error: "Missing refresh token" }, { status: 401 });
  }

  const res = await fetch(`${API_URL}/api/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  const data = await res.json();
  if (!res.ok) {
    return NextResponse.json(data, { status: res.status });
  }

  const response = NextResponse.json({ ok: true });
  response.cookies.set("access_token", data.access_token, {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
    secure: isProd,
  });
  response.cookies.set("refresh_token", data.refresh_token, {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
    secure: isProd,
  });
  return response;
}
