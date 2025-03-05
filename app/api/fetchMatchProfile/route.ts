import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// GET: 現在のログインユーザーの情報を取得
export async function GET(req: NextRequest) {
  // 認証情報を取得（ここはログインができたら実装、一旦user_idを普通に渡す）
  // const { data: { user }, error: authError } = await supabase.auth.getUser();

  // if (authError || !user) {
  //   return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  // }

  // const userId = user.id;
  const userId = "61ecfa1e-6208-4093-ab93-9318f137b0ad";

  // Supabase から `user_attributes` テーブルのデータを取得
  const { data, error } = await supabase
    .from("user_attributes")
    .select("*")
    .eq("user_id", userId)
    .single(); // 1つのレコードのみ取得

  if (error || !data) {
    return NextResponse.json({ error: error?.message || "User not found" }, { status: 404 });
  }

  return NextResponse.json(data, { status: 200 });
}
