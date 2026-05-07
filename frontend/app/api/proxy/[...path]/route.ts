import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import type { NextRequest } from "next/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function forward(request: NextRequest) {
  const accessToken = cookies().get("access_token")?.value;
  if (!accessToken) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const targetUrl = `${API_URL}/api${request.nextUrl.pathname.replace("/api/proxy", "")}${
    request.nextUrl.search
  }`;

  const res = await fetch(targetUrl, {
    method: request.method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: request.method === "GET" ? undefined : await request.text(),
  });

  const data = await res.text();
  return new NextResponse(data, { status: res.status, headers: { "Content-Type": "application/json" } });
}

export async function GET(request: NextRequest) {
  return forward(request);
}

export async function POST(request: NextRequest) {
  return forward(request);
}

export async function PATCH(request: NextRequest) {
  return forward(request);
}

export async function DELETE(request: NextRequest) {
  return forward(request);
}
