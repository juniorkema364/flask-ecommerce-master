// import { create } from "zustand";
// import axios from "../lib/axios";
// import { toast } from "react-hot-toast";
 


// export const useAdminStore = create((set) => ({
//     user : null ,
//     loading : false , 
//     checkingAuth : true , 

//     admin_signup : async ({admin_name , admin_email , admin_password , confirmPassword}) => {
//         set({ loading : true});
    
//         if (admin_password !== confirmPassword) {
//             set({ loading : false }); 
//             return toast.error('les mots de passes ne correspondent pas , veillez ressayer'); 
//         }
    
//         try  {
//             const res = await axios.post('/auth/admin' , {admin_name , admin_email , admin_password});
//             set({
//                 user : res.data , 
//                 loading : false , 
//             })
//         }

//         catch (error) {
//             set({ loading: false}) ; 
//             toast.error(error.response.data.message);
//         }
    
//     }, 

//     login : async (admin_email , admin_password) => {
//         set ({ loading : true}) ; 

//         try  {
//             const res = await axios.post('/auth/login' , {admin_email , admin_password});

//             set ({
//                 user : res.data , 
//                 loading  : false ,
//             })
//         }

//         catch(error) {
//             set ({ loading : false });
//             toast.error(error.response.data.message);
//         }
//     } , 

//     logout : async () => {
//         try { 
//             await axios.post('/auth/logout');
//             set({user : null});
//         } catch(error) {
//             toast.error(error.response?.data?.message);
//         }
//     }
    
// }));

