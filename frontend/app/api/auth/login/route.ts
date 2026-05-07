import { NextResponse } from "next/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function POST(request: Request) {
  const payload = await request.json();
  const res = await fetch(`${API_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!res.ok) {
    return NextResponse.json(data, { status: res.status });
  }

  const response = NextResponse.json({ user: data.user });
  response.cookies.set("access_token", data.tokens.access_token, {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
  });
  response.cookies.set("refresh_token", data.tokens.refresh_token, {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
  });
  return response;
}
