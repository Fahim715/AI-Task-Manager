import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const url = new URL("/login", request.url);
  const response = NextResponse.redirect(url);
  response.cookies.set("access_token", "", { httpOnly: true, path: "/", maxAge: 0 });
  response.cookies.set("refresh_token", "", { httpOnly: true, path: "/", maxAge: 0 });
  return response;
}
