"use client";

import { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

const fields = ["公共", "技統本", "TC&S", "金融", "法人"];

export default function UserList() {
  const [selectedField, setSelectedField] = useState<string>(fields[0]);
  const [users, setUsers] = useState<{ name: string }[]>([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        // `user_attributes` テーブルから選択された `field` の `user_id` を取得
        const { data: userIdsData, error: userIdsError } = await supabase
          .from("user_attributes")
          .select("user_id")
          .eq("field", selectedField);

        if (userIdsError) throw userIdsError;

        const userIds = userIdsData.map((item) => item.user_id);

        if (userIds.length === 0) {
          setUsers([]);
          return;
        }

        // `users` テーブルから 上記のidを持つ`name` を取得
        const { data: usersData, error: usersError } = await supabase
          .from("users")
          .select("name")
          .in("id", userIds);

        if (usersError) throw usersError;

        setUsers(usersData || []);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    fetchUsers();
  }, [selectedField]);

  return (
    <div>
      <h1>ユーザーリスト</h1>
      <select value={selectedField} onChange={(e) => setSelectedField(e.target.value)}>
        {fields.map((field) => (
          <option key={field} value={field}>{field}</option>
        ))}
      </select>
      <ul>
        {users.length > 0 ? (
          users.map((user, index) => <li key={index}>{user.name}</li>)
        ) : (
          <li>該当するユーザーがいません</li>
        )}
      </ul>
    </div>
  );
}
