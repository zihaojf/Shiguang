import {clearTokens} from '@/api/auth'
import router from '@/router'

export function logout(){
  clearTokens()
  router.push('/login')
}
