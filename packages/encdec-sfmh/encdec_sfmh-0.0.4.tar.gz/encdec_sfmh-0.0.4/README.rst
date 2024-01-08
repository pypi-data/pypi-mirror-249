EncDec
==========

**EncDec** is a package that allows users to encrypt and decrypt string data using a unique key of your choice. 

Here is a simple example:

.. code-block:: python

   from encdec_sfmh.encdec import *

   original = 'rusksarenice'

   print(f'Original: {original}')

   # Keyless encryption and decryption
   print(f'\nEncryptedv1: {encsimple(original)}')
   print(f'Decryptedv1: {decsimple(encsimple(original))}')

   # Complex encryption and decryption with a key
   toPrint = enccomplex(original,key='coffee')
   print('\nEncryptedv2:', toPrint)
   print('Decryptedv2:', deccomplex(toPrint,key='coffee'))

**Giving developers more control over their encryptions**