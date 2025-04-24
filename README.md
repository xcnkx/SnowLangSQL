## SnowLangSQL

このアプリでは、自然言語を使用して Snowflake データベースにクエリを実行できます。対話履歴もサポートしています。

## Requirements

- uv
- OpenAI API キー
- Snowflake Key-Pair 認証用の秘密鍵（RSA 形式）（オプション - SSO 認証も可能）

### インストール

1. `.env`ファイルを作成し、以下の環境変数を設定します。

```
SNOWFLAKE_ACCOUNT=<your_snowflake_account>
SNOWFLAKE_USER=<your_snowflake_user>
SNOWFLAKE_DATABASE=<your_snowflake_database>
SNOWFLAKE_SCHEMA=<your_snowflake_schema>
SNOWFLAKE_WAREHOUSE=<your_snowflake_warehouse>
SNOWFLAKE_ROLE=<your_snowflake_role>  # 使用するロールを指定（オプション）
SNOWFLAKE_PRIVATE_KEY_PATH=<path_to_private_key_file>  # Key-Pair認証の場合のみ設定
SNOWFLAKE_PRIVATE_KEY_PASSPHRASE=<private_key_passphrase>  # 秘密鍵にパスフレーズがある場合
OPENAI_API_KEY=<your_openai_api_key>
```

2. make コマンドを使用してインストールします。

```
make install
```

3. アプリを起動します。

```
make run
```

### Snowflake 認証方式について

このアプリは Snowflake への接続に以下の認証方式をサポートしています：

#### 1. Key-Pair 認証

秘密鍵を使用した認証方式です。以下の手順で設定してください：

1. RSA 鍵ペアを生成します（既に持っている場合はスキップ）：

   ```
   openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8
   ```

   パスフレーズを設定する場合は、プロンプトに従って入力してください。

2. 公開鍵を抽出します：

   ```
   openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
   ```

3. Snowflake で公開鍵を登録します：

   ```sql
   ALTER USER <username> SET RSA_PUBLIC_KEY='<public_key_content>';
   ```

   `<public_key_content>`には、rsa_key.pub ファイルの内容（BEGIN/END の行を含む）を貼り付けます。

4. `.env`ファイルに秘密鍵のパスとパスフレーズ（設定した場合）を指定します。

#### 2. SSO 認証（externalbrowser）

ブラウザを使用した SSO 認証方式です。以下の手順で設定してください：

1. `.env`ファイルで `SNOWFLAKE_PRIVATE_KEY_PATH` を設定しないか、空にします。
2. アプリ起動時に自動的にブラウザが開き、Snowflake の SSO 認証ページが表示されます。
3. SSO 認証を完了すると、アプリが Snowflake に接続されます。

### Screenshot

![Screenshot](imgs/demo.png)

### 注意

- このアプリは、[OpenAI API](https://beta.openai.com/signup/)を使用しています。API キーを取得してください。
- このアプリは、[Snowflake](https://www.snowflake.com/)データベースに接続します。アカウントを作成し、データベースをセットアップしてください。
- Snowflake 認証は Key-Pair 方式または SSO 方式を使用します。詳細は[Snowflake のドキュメント](https://docs.snowflake.com/en/user-guide/key-pair-auth)を参照してください。
