// A retry first asks for the immutable receipt. An absent receipt is usable
// only after the current target has been authorized again; transport/proxy
// failures never authorize another dispatch. The caller retains the command.
export async function recoverOperation(
  lookup: () => Promise<any>, authorize: () => Promise<any>, resend: () => Promise<any>,
) {
  try { return await lookup(); }
  catch (error: any) {
    if (error?.status !== 404 || error.apiDetail !== 'Tilgangen ble avvist.') throw error;
    await authorize();
    return resend();
  }
}
