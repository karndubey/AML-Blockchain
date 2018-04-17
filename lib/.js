/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * Sample transaction processor function.
 * @param {org.acme.model.createKyc}tx The sample transaction instance.
 *
 * @transaction
 */
function createBlock(tx) {
    
    var bankArr = [];
  	 for(var i=0; i<tx.asset.bank.length; i++)
    {
      bankArr.push(tx.asset.bank[i]);
    }
    bankArr.push(tx.bank);

    // Update the asset with the new value.
    tx.asset.bank = bankArr;
    // Get the asset registry for the asset.
    return getAssetRegistry('org.acme.model.KYCAsset')
        .then(function (assetRegistry) {

            // Update the asset in the asset registry.
            return assetRegistry.update(tx.asset);

        });

}
/**
 @param {org.acme.model.add_suspicious_transaction}transfer The sample transaction instance.
 @transaction
*/
function addSuspiciousTransaction(transfer) {
    return getAssetRegistry('org.acme.model.TransactionDetails')
    .then(function (assetRegistry) {

        // Update the asset in the asset registry.
        return assetRegistry.update(transfer.tranx);

    });

}
function getUID(id){
    var request = require('request')
	return request.get('http://40.83.126.91:3000/api/org.acme.land.registry.Property/'+id, function(res, err)  {
	console.log(err.body);
 }); 
}
