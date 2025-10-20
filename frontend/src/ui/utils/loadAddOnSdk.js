// src/ui/utils/loadAddOnSdk.js
let sdk = null;

export const loadAddOnSdk = async () => {
  if (sdk) return sdk;
  const module = await import(/* webpackIgnore: true */ "https://new.express.adobe.com/static/add-on-sdk/sdk.js");
  await module.default.ready;
  sdk = module.default;
  return sdk;
};
