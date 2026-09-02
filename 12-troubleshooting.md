[← Docs index](README.md)

# 12 — Troubleshooting

## Pretty URLs 404 (`/product/xyz` not found)

`mod_rewrite` is off, or `.htaccess` is being ignored.

- Confirm `.htaccess` uploaded (it starts with a dot — many FTP clients hide it)
- Ask your host to enable `mod_rewrite`
- On Apache, `AllowOverride All` must be set for your directory
- Testing locally? Use `php -S 0.0.0.0:8080 router.php` — plain `php -S` has no
  rewrite support

Query-string URLs (`/product.php?slug=xyz`) keep working either way.

## Blank white page

PHP is erroring with display off. Check your host's error log. Most common
causes:

- PHP older than 8.1
- `pdo_sqlite` not enabled
- `db/` not writable

## "Unable to open database file"

`db/` is not writable. Set it to `755` (or `775` on stricter hosts) and make
sure `db/voltra.sqlite` itself is writable.

## Images upload but do not appear

`uploads/` is not writable, or the path is wrong. Check the file exists on
disk, then open its URL directly. If you get 403, your host may be blocking
the folder.

## Logo or favicon not showing

Set both in **Settings → Site identity**, then hard-refresh (`Ctrl+F5`).
Browsers cache favicons aggressively — try a private window to confirm.

## Emails not sending

- Check port: **587** for STARTTLS, **465** for SSL
- Many shared hosts block outbound SMTP — use their relay, or a service like
  Brevo or Mailgun
- Gmail needs an **app password**, not your account password
- Use **Send test email** to see the actual error

## Payment succeeds but the order stays unpaid

The gateway callback is not reaching you.

- Razorpay: check the webhook URL and that the secret matches exactly
- PayPal: confirm live/sandbox matches your keys
- The callback must be publicly reachable — it will not work on localhost

## Vendor sees "not your resource"

Working as intended. A vendor can only touch their own products, orders and
packages. If they genuinely need access, the record is assigned to another
seller — check the product's **Seller** field.

## Save shows a blank page

Fixed in the current build — panel screens buffer their output so a
redirect-after-save always fires. If you see it, you are on an older copy.

## Countdown timer not appearing

The timer only renders while the deal is **in the future**. Check **Deal ends**
in the product editor is set and has not passed. It also needs the product to
be discounted (MRP above price) to look right.

## Everything looks unstyled

`assets/css/app.css` is not loading. Open its URL directly — a 404 means the
upload was incomplete; a 403 means permissions.

## Getting more detail

Temporarily add this to the top of `includes/config.php`:

```php
ini_set('display_errors', '1');
error_reporting(E_ALL);
```

**Remove it once you are done.** Never leave error display on in production —
it leaks file paths and query structure.

---

[← Backup & restore](11-backup.md) · [Docs index](README.md)
