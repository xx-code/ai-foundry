import type { ApiRouteDefinition } from "~/types/shared/routes"

export class ApiLinkBuilder<TResponse = any, TMapped = TResponse> {
    private url: string
    private httpMethod: ApiRouteDefinition['method']
    private bodyData?: any
    private queryData?: any
    private formDataPayload?: FormData
    private mapperFn?: (data: TResponse) => TMapped

    constructor(route: ApiRouteDefinition) {
        this.url = route.serverPath
        this.httpMethod = route.method
    }

    public static route<T = any>(route: ApiRouteDefinition): ApiLinkBuilder<T, T> {
        return new ApiLinkBuilder<T, T>(route)
    }

    public params(params: Record<string, string | number>): this {
        Object.entries(params).forEach(([key, value]) => {
            this.url = this.url.replace(`:${key}`, String(value)) 
        })
        return this
    }

    public method(method: ApiRouteDefinition['method']): this {
        this.httpMethod = method
        return this
    }

    public body(data: any): this {
        this.bodyData = data
        this.formDataPayload = undefined // Réinitialise formData pour éviter tout conflit
        return this
    }

    /**
     * Permet de passer directement une instance de FormData
     * ou d'en construire une à partir d'un objet simple (clé-valeur / File).
     */
    public formData(data: FormData | Record<string, any>): this {
        if (data instanceof FormData) {
            this.formDataPayload = data
        } else {
            const fd = new FormData()
            Object.entries(data).forEach(([key, value]) => {
                if (value !== undefined && value !== null) {
                    if (value instanceof File || value instanceof Blob) {
                        fd.append(key, value)
                    } else if (Array.isArray(value)) {
                        value.forEach((item) => fd.append(`${key}[]`, item))
                    } else {
                        fd.append(key, String(value))
                    }
                }
            })
            this.formDataPayload = fd
        }
        this.bodyData = undefined // Réinitialise body JS standard pour éviter les conflits
        return this
    }

    public query(data: any): this {
        this.queryData = data
        return this
    }

    public mapper<R>(fn: (data: TResponse) => R): ApiLinkBuilder<TResponse, R> {
        this.mapperFn = fn as any
        return this as any
    }

    public buildOptions() {
        return {
            url: this.url,
            method: this.httpMethod === '*' ? undefined : this.httpMethod,
            body: this.formDataPayload ?? this.bodyData,
            query: this.queryData
        }
    }

    public async execute(): Promise<TMapped> {
        const options = this.buildOptions()
        
        // $fetch (ofetch) détecte automatiquement une instance FormData et définit 
        // le Content-Type approprie (multipart/form-data) avec le bon boundary.
        const res = await $fetch<TResponse>(options.url, {
            method: options.method,
            body: options.body,
            query: options.query
        })

        return this.mapperFn ? this.mapperFn(res) : (res as unknown as TMapped)
    }
}